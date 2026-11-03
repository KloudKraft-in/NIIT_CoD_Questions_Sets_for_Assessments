import importlib.util
import os
import sys
import pandas as pd
import random

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable."
    return True, None

# Embedded Reference Logic for Grading (QD-720 / QP-213 Style)
class _GradingLogic:
    @staticmethod
    def get_at_risk_skus(df_s):
        at_risk = df_s[df_s['Stock'] < df_s['Safety']]
        return sorted(at_risk['SKU'].unique().tolist())

    @staticmethod
    def calc_mean_lead_time(df_l):
        df = df_l.copy()
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])
        df['lead_time'] = (df['Delivery_Date'] - df['Order_Date']).dt.days
        return round(float(df['lead_time'].mean()), 1)

    @staticmethod
    def carrier_return_rate(df_l):
        total = df_l.groupby('Carrier').size()
        returned = df_l[df_l['Status'] == 'Returned'].groupby('Carrier').size()
        rate = (returned / total * 100).fillna(0)
        return {k: round(float(v), 2) for k, v in rate.to_dict().items()}

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    # Load Student Solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        msg = f"IMPORT ERROR: {e}"
        print(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write(msg + "\n")
        return

    print("Running Tests for: Supply Chain Optimizer (Professional Expansion)\n")
    report_lines = ["Running Tests for: Supply Chain Optimizer (Professional Expansion)\n"]

    if not hasattr(solution, "WarehouseManager"):
        msg = "ERROR: WarehouseManager class not found in solution.py"
        print(msg); report_lines.append(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")
        return

    # Data Paths
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    stock_p = os.path.join(data_dir, "warehouse_stock.csv")
    logs_p = os.path.join(data_dir, "shipping_logs.csv")
    
    try:
        raw_stock = pd.read_csv(stock_p)
        raw_logs = pd.read_csv(logs_p)
    except Exception as e:
        print(f"CRITICAL ERROR: Data missing. {e}"); return

    def compare_rounded(r, e, precision=1):
        try:
            if isinstance(r, (float, int)): return round(float(r), precision) == round(float(e), precision)
            if isinstance(r, dict):
                return all(compare_rounded(r[k], e.get(k)) for k in e)
            if isinstance(r, list):
                return all(compare_rounded(x, y) for x, y in zip(r, e))
            return str(r) == str(e)
        except: return False

    test_cases = [
        {
            "desc": "Initialize and Load internal DataFrames",
            "func": "load_data",
            "setup": lambda: solution.WarehouseManager(),
            "call": lambda obj: (obj.load_data(stock_p, logs_p), isinstance(obj.df_stock, pd.DataFrame)),
            "check": lambda res: res[1] == True,
            "expected_output": "WarehouseManager.df_stock should be a DataFrame after loading.",
            "marks": 0
        },
        {
            "desc": "Verify Inner Join merging logic",
            "func": "get_merged_data",
            "setup": lambda: _inject_data(solution.WarehouseManager(), raw_stock, raw_logs),
            "call": lambda obj: len(obj.get_merged_data()),
            "check": lambda res: res == len(pd.merge(raw_stock, raw_logs, on=['SKU', 'Warehouse_ID'], how='inner')),
            "expected_output": "Merged DataFrame count matches inner join on SKU and Warehouse_ID.",
            "marks": 3
        },
        {
            "desc": "Filter sub-safety stock items",
            "func": "get_at_risk_skus",
            "setup": lambda: solution.SupplyOptimizer(),
            "call": lambda obj: obj.get_at_risk_skus(raw_stock),
            "check": lambda res: res == _GradingLogic.get_at_risk_skus(raw_stock),
            "expected_output": "Sorted list of SKUs where Stock < Safety.",
            "marks": 3
        },
        {
            "desc": "Average transit days calculation",
            "func": "calc_mean_lead_time",
            "setup": lambda: solution.SupplyOptimizer(),
            "call": lambda obj: obj.calc_mean_lead_time(raw_logs),
            "check": lambda res: compare_rounded(res, _GradingLogic.calc_mean_lead_time(raw_logs)),
            "expected_output": "Mean of (Delivery_Date - Order_Date) in days.",
            "marks": 3
        },
        {
            "desc": "Aggregate total inventory financial value",
            "func": "total_inventory_value",
            "setup": lambda: solution.SupplyOptimizer(),
            "call": lambda obj: obj.total_inventory_value(raw_stock),
            "check": lambda res: compare_rounded(res, (raw_stock['Stock'] * raw_stock['Cost']).sum()),
            "expected_output": "Sum of (Stock * Cost) across all items.",
            "marks": 3
        },
        {
            "desc": "Grouped return rate analysis",
            "func": "carrier_return_rate",
            "setup": lambda: solution.SupplyOptimizer(),
            "call": lambda obj: obj.carrier_return_rate(raw_logs),
            "check": lambda res: compare_rounded(res, _GradingLogic.carrier_return_rate(raw_logs)),
            "expected_output": "Dictionary of Carriers and their return percentage.",
            "marks": 4
        },
        {
            "desc": "Multi-metric summary object",
            "func": "generate_summary",
            "setup": lambda: solution.SupplyOptimizer(),
            "call": lambda obj: obj.generate_summary(raw_stock, raw_logs),
            "check": lambda res: res.get('total_skus') == raw_stock['SKU'].nunique() and 'best_carrier' in res,
            "expected_output": "Dict with total_skus, critical_count, and best_carrier.",
            "marks": 4
        }
    ]

    total_score = 0
    for idx, case in enumerate(test_cases, 1):
        marks = case["marks"]
        try:
            obj = case["setup"]()
            valid, err = validate_method_exists(obj, case["func"])
            if not valid:
                msg = f"FAIL TC{idx} [{case['desc']}]: {err}"
                print(msg); report_lines.append(msg); continue

            result = case["call"](obj)
            passed = case["check"](result)

            if passed:
                total_score += marks
                msg = f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})"
            else:
                msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks})\n  Expected: {case['expected_output']}\n  Got: {repr(result)}"
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks}) | Error: {type(e).__name__}: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/20.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

def _inject_data(obj, s, l):
    obj.df_stock = s.copy()
    obj.df_logs = l.copy()
    return obj

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
