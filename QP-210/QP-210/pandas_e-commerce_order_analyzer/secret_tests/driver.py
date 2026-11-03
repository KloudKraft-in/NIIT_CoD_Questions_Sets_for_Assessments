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
    except Exception as e:
        error_msg = f"IMPORT ERROR: {str(e)}\nMake sure all required modules are imported correctly"
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return
    
    print("Running Tests for: E-Commerce Order Analyzer\n")
    report_lines = ["Running Tests for: E-Commerce Order Analyzer\n"]
    
    # Verify class exists
    if not hasattr(solution, "OrderAnalyzer"):
        error_msg = "ERROR: OrderAnalyzer class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return
    
    OrderAnalyzer = solution.OrderAnalyzer
    
    # Data file path
    data_file = os.path.join(os.path.dirname(__file__), "..", "data", "orders.csv")
    
    test_cases = [
        {
            "desc": "Initialize and check empty state",
            "func": "__init__",
            "setup": lambda: _setup_tc1(OrderAnalyzer),
            "call": lambda obj: obj.df is None or len(obj.df) == 0,
            "check": lambda result: result == True,
            "expected_output": "self.df is None or empty",
            "marks": 2
        },
        {
            "desc": "Load data and verify row count",
            "func": "load_data",
            "setup": lambda: _setup_tc2(OrderAnalyzer, data_file),
            "call": lambda obj: len(obj.df),
            "check": lambda result: result == 10,
            "expected_output": "DataFrame with 10 rows",
            "marks": 2
        },
        {
            "desc": "Verify Revenue column exists",
            "func": "calculate_revenue",
            "setup": lambda: _setup_tc3(OrderAnalyzer, data_file),
            "call": lambda obj: (obj.calculate_revenue(), 'Revenue' in obj.df.columns),
            "check": lambda result: result[1] == True,
            "expected_output": "'Revenue' column added",
            "marks": 3
        },
        {
            "desc": "Check total revenue calculation",
            "func": "calculate_revenue",
            "setup": lambda: _setup_tc4(OrderAnalyzer, data_file),
            "call": lambda obj: obj.calculate_revenue(),
            "check": lambda result: abs(result - 4035.0) < 0.01,
            "expected_output": "Total revenue = 4035.0",
            "marks": 3.5
        },
        {
            "desc": "Category quantity breakdown",
            "func": "category_quantity",
            "setup": lambda: _setup_tc5(OrderAnalyzer, data_file),
            "call": lambda obj: obj.category_quantity(),
            "check": lambda result: result == {'Electronics': 18, 'Books': 7, 'Clothing': 6},
            "expected_output": "{'Electronics': 18, 'Books': 7, 'Clothing': 6}",
            "marks": 3.5
        },
        {
            "desc": "Filter orders above 500 revenue",
            "func": "filter_orders",
            "setup": lambda: _setup_tc6(OrderAnalyzer, data_file),
            "call": lambda obj: obj.filter_orders(500),
            "check": lambda result: result == [101, 103, 107],
            "expected_output": "[101, 103, 107]",
            "marks": 3
        },
        {
            "desc": "Check count of filtered orders",
            "func": "filter_orders",
            "setup": lambda: _setup_tc7(OrderAnalyzer, data_file),
            "call": lambda obj: len(obj.filter_orders(500)),
            "check": lambda result: result == 3,
            "expected_output": "3 orders match filter",
            "marks": 3
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 1)
        max_score += marks
        
        try:
            # Verify method exists
            method_exists, error_msg = validate_method_exists(OrderAnalyzer(), case["func"])
            if not method_exists and case["func"] != "__init__":
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
                msg += f"  Hint: Review the method implementation and logic"
            
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check method implementation, data file path, and error handling"
            print(msg)
            report_lines.append(msg)

    # ============ FINAL SCORING ============
    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    if total_score == 0:
        score_line += "\n[Warning] No tests passed. Check method implementations and CSV file loading."
    
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_tc1(OrderAnalyzer):
    """TC1 Setup: Initialize and check empty state - Independent fresh instance."""
    return OrderAnalyzer()


def _setup_tc2(OrderAnalyzer, data_file):
    """TC2 Setup: Load data and verify row count - Independent fresh instance."""
    analyzer = OrderAnalyzer()
    analyzer.load_data(data_file)
    return analyzer


def _setup_tc3(OrderAnalyzer, data_file):
    """TC3 Setup: Verify Revenue column exists - Independent fresh instance."""
    analyzer = OrderAnalyzer()
    analyzer.load_data(data_file)
    return analyzer


def _setup_tc4(OrderAnalyzer, data_file):
    """TC4 Setup: Check total revenue calculation - Independent fresh instance."""
    analyzer = OrderAnalyzer()
    analyzer.load_data(data_file)
    return analyzer


def _setup_tc5(OrderAnalyzer, data_file):
    """TC5 Setup: Category quantity breakdown - Independent fresh instance."""
    analyzer = OrderAnalyzer()
    analyzer.load_data(data_file)
    # Ensure Revenue column created first
    analyzer.calculate_revenue()
    return analyzer


def _setup_tc6(OrderAnalyzer, data_file):
    """TC6 Setup: Filter orders above 500 revenue - Independent fresh instance."""
    analyzer = OrderAnalyzer()
    analyzer.load_data(data_file)
    # Ensure Revenue column created first
    analyzer.calculate_revenue()
    return analyzer


def _setup_tc7(OrderAnalyzer, data_file):
    """TC7 Setup: Check count of filtered orders - Independent fresh instance."""
    analyzer = OrderAnalyzer()
    analyzer.load_data(data_file)
    # Ensure Revenue column created first
    analyzer.calculate_revenue()
    return analyzer


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solution_path = sys.argv[1]
    else:
        solution_path = os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.py')
    test_student_code(solution_path)
