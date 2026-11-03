import importlib.util
import os
import inspect
import numpy as np

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "mock_sales.csv")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    print("Running Tests for: Store Sales Monitor\n")
    report_lines = ["Running Tests for: Store Sales Monitor\n"]

    test_cases = [
        {
            "desc": "Load mock_sales.csv and verify 15 rows loaded",
            "func": "load_data",
            "setup": lambda: (lambda obj: (obj.load_data(data_dir), obj)[-1])(student_module.SalesMonitor()),
            "call": lambda obj: len(obj.df),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 15,
            "marks": 3
        },
        {
            "desc": "Verify 'Revenue' column is created after calculate_revenue()",
            "func": "calculate_revenue",
            "setup": lambda: (lambda obj: (obj.load_data(data_dir), obj.calculate_revenue(), obj)[-1])(student_module.SalesMonitor()),
            "call": lambda obj: 'Revenue' in obj.df.columns,
            "check": lambda result: result is True,
            "marks": 3
        },
        {
            "desc": "Check Revenue calculation for ORD001 (Qty=2, Price=500, Expected=1000)",
            "func": "calculate_revenue",
            "setup": lambda: (lambda obj: (obj.load_data(data_dir), obj.calculate_revenue(), obj)[-1])(student_module.SalesMonitor()),
            "call": lambda obj: obj.df[obj.df['OrderID'] == 'ORD001']['Revenue'].values[0],
            "check": lambda result: isinstance(result, (int, float, np.integer, np.floating)) and abs(result - 1000) < 0.01,
            "marks": 2
        },
        {
            "desc": "Get total revenue for 'North' region (Expected=3475.0)",
            "func": "get_total_by_region",
            "setup": lambda: (lambda obj: (obj.load_data(data_dir), obj.calculate_revenue(), obj)[-1])(student_module.SalesMonitor()),
            "call": lambda obj: obj.get_total_by_region("North"),
            "check": lambda result: isinstance(result, (int, float, np.integer, np.floating)) and abs(result - 3475.0) < 0.01,
            "marks": 3
        },
        {
            "desc": "Search for revenue in 'Unknown' region (Expected=0.0)",
            "func": "get_total_by_region",
            "setup": lambda: (lambda obj: (obj.load_data(data_dir), obj.calculate_revenue(), obj)[-1])(student_module.SalesMonitor()),
            "call": lambda obj: obj.get_total_by_region("Unknown"),
            "check": lambda result: isinstance(result, (int, float, np.integer, np.floating)) and abs(result - 0.0) < 0.01,
            "marks": 2
        },
        {
            "desc": "Count bulk orders with Qty >= 10 (Expected=3)",
            "func": "filter_bulk_orders",
            "setup": lambda: (lambda obj: (obj.load_data(data_dir), obj)[-1])(student_module.SalesMonitor()),
            "call": lambda obj: obj.filter_bulk_orders(10),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 3,
            "marks": 3
        },
        {
            "desc": "Verify top product by quantity sold (Expected='Charger')",
            "func": "top_product_name",
            "setup": lambda: (lambda obj: (obj.load_data(data_dir), obj)[-1])(student_module.SalesMonitor()),
            "call": lambda obj: obj.top_product_name(),
            "check": lambda result: isinstance(result, str) and result == "Charger",
            "marks": 2
        },
        {
            "desc": "Verify top product 'Charger' total qty is 35",
            "func": "top_product_name",
            "setup": lambda: (lambda obj: (obj.load_data(data_dir), obj)[-1])(student_module.SalesMonitor()),
            "call": lambda obj: obj.df[obj.df['Product'] == 'Charger']['Qty'].sum(),
            "check": lambda result: isinstance(result, (int, np.integer)) and result == 35,
            "marks": 2
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2)
        is_hidden = case.get("is_hidden", False)
        
        if not is_hidden:
            max_score += marks
        
        try:
            obj = case["setup"]()
            
            # Check for pass-only implementation
            func = getattr(obj, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()
            if 'pass' in src and len(src) < 80:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue
            
            # Execute test
            result = case["call"](obj)
            passed = case["check"](result)
            
            if passed:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"PASS {test_type} Test Case {idx} Passed: {case['desc']}"
                if not is_hidden:
                    total_score += marks
            else:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"
            
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            test_type = "Hidden" if is_hidden else "Visible"
            msg = f"FAIL {test_type} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/20.0 (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
