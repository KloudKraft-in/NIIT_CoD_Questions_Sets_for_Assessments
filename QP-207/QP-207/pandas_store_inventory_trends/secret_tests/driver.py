import pandas as pd
import os
import sys
import importlib.util

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found in class. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable. Make sure it's defined as a method."
    return True, None

def test_student_code(solution_path):
    """Main test function that runs all test cases"""
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    # Clear previous report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("")

    # Load the student's solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(solution)
    except SyntaxError as e:
        error_msg = f"SYNTAX ERROR: {str(e)}\nFix the syntax error in solution.py before running tests."
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return
    except ImportError as e:
        error_msg = f"IMPORT ERROR: {str(e)}\nMake sure pandas is imported correctly in solution.py"
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return
    
    print("Running Tests for: Store Inventory Trends\n")
    report_lines = ["Running Tests for: Store Inventory Trends\n"]
    
    # Verify class exists
    if not hasattr(solution, "InventoryTrends"):
        error_msg = "ERROR: InventoryTrends class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return
    
    InventoryTrends = solution.InventoryTrends
    
    # Get the data path
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    store_csv = os.path.join(data_dir, 'store_data.csv')
    
    test_cases = [
        {
            "desc": "Check state before loading CSV",
            "func": "initialize",  # Skip method check for init
            "setup": lambda: InventoryTrends(),
            "call": lambda obj: obj.df,
            "check": lambda result: result is None,
            "expected_output": "df attribute should be None initially",
            "marks": 2
        },
        {
            "desc": "Load store_data.csv and check row count",
            "func": "load_inventory",
            "setup": lambda: InventoryTrends(),
            "call": lambda obj: (obj.load_inventory(store_csv), len(obj.df)),
            "check": lambda result: result[1] == 12,
            "expected_output": "DataFrame should have 12 rows",
            "marks": 2
        },
        {
            "desc": "Add 'Valuation' column and check name",
            "func": "calculate_valuation",
            "setup": lambda: _setup_valuation_column(InventoryTrends, store_csv),
            "call": lambda obj: "Valuation" in obj.df.columns,
            "check": lambda result: result == True,
            "expected_output": "Valuation column should exist in DataFrame",
            "marks": 2
        },
        {
            "desc": "Check total valuation sum",
            "func": "calculate_valuation",
            "setup": lambda: _setup_calculate_valuation(InventoryTrends, store_csv),
            "call": lambda obj: obj.calculate_valuation(),
            "check": lambda result: result == 13250.0,
            "expected_output": "Total valuation should be 13250.0",
            "marks": 4
        },
        {
            "desc": "Category mean stock (Apparel category)",
            "func": "category_mean_stock",
            "setup": lambda: _setup_category_mean(InventoryTrends, store_csv),
            "call": lambda obj: obj.category_mean_stock(),
            "check": lambda result: isinstance(result, dict) and result.get("Apparel") == 46.25,
            "expected_output": "Category mean dict with Apparel mean = 46.25",
            "marks": 4
        },
        {
            "desc": "Find items with StockLevel < 10",
            "func": "get_reorder_list",
            "setup": lambda: _setup_reorder_list(InventoryTrends, store_csv),
            "call": lambda obj: obj.get_reorder_list(10),
            "check": lambda result: sorted(result) == ['S03', 'S06', 'S10', 'S12'],
            "expected_output": "ProductID list with StockLevel < 10: ['S03', 'S06', 'S10', 'S12']",
            "marks": 3
        },
        {
            "desc": "Check count of Reorder IDs list",
            "func": "get_reorder_list",
            "setup": lambda: _setup_reorder_count(InventoryTrends, store_csv),
            "call": lambda obj: len(obj.get_reorder_list(10)),
            "check": lambda result: result == 4,
            "expected_output": "Reorder list should have 4 items",
            "marks": 3
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 3)
        max_score += marks
        
        try:
            # Verify method exists (skip for initialization)
            if case["func"] != "initialize":
                method_exists, error_msg = validate_method_exists(InventoryTrends(), case["func"])
                if not method_exists:
                    msg = f"FAIL TC{idx} [{case['desc']}]: {error_msg}"
                    print(msg)
                    report_lines.append(msg)
                    continue
            
            # Setup and execute test
            obj = case["setup"]()
            result = case["call"](obj)
            passed = case["check"](result)
            
            if passed:
                msg = f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})"
                total_score += marks
            else:
                # Provide detailed mismatch error
                msg = f"FAIL TC{idx} [{case['desc']}]\n"
                msg += f"  Expected: {case['expected_output']}\n"
                msg += f"  Got: {repr(result)}\n"
                msg += f"  Hint: Review the method implementation and data types"
            
            print(msg)
            report_lines.append(msg)
        
        except FileNotFoundError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: File Not Found\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Make sure store_data.csv exists in the data folder"
            print(msg)
            report_lines.append(msg)
        
        except AttributeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Attribute Not Found\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check the method implementation - ensure DataFrame operations are correct"
            print(msg)
            report_lines.append(msg)
        
        except TypeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Type Mismatch Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check method return types - calculate_valuation() should return float, category_mean_stock() should return dict, get_reorder_list() should return list"
            print(msg)
            report_lines.append(msg)
        
        except ValueError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Value Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check your data processing logic"
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Review implementation for logic errors. Check method signatures match specification"
            print(msg)
            report_lines.append(msg)

    # ============ FINAL SCORING ============
    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    if total_score == 0:
        score_line += "\n⚠️ No tests passed. Make sure to implement all required methods with correct signatures."
    
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_valuation_column(InventoryTrends, store_csv):
    """Setup for valuation column test - Independent fresh instance."""
    trends = InventoryTrends()
    trends.load_inventory(store_csv)
    trends.calculate_valuation()
    return trends


def _setup_calculate_valuation(InventoryTrends, store_csv):
    """Setup for calculate valuation test - Independent fresh instance."""
    trends = InventoryTrends()
    trends.load_inventory(store_csv)
    return trends


def _setup_category_mean(InventoryTrends, store_csv):
    """Setup for category mean test - Independent fresh instance."""
    trends = InventoryTrends()
    trends.load_inventory(store_csv)
    return trends


def _setup_reorder_list(InventoryTrends, store_csv):
    """Setup for reorder list test - Independent fresh instance."""
    trends = InventoryTrends()
    trends.load_inventory(store_csv)
    return trends


def _setup_reorder_count(InventoryTrends, store_csv):
    """Setup for reorder count test - Independent fresh instance."""
    trends = InventoryTrends()
    trends.load_inventory(store_csv)
    return trends


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solution_path = sys.argv[1]
    else:
        solution_path = os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.py')
    test_student_code(solution_path)
