import importlib.util
import os
import sys
from io import StringIO

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found in class. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable. Make sure it's defined as a method."
    return True, None

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    # Clear previous report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("")

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(student_module)
    except SyntaxError as e:
        error_msg = f"SYNTAX ERROR: {str(e)}\nFix the syntax error in solution.py before running tests."
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return

    print("Running Tests for: Customer Account Operations\n")
    report_lines = ["Running Tests for: Customer Account Operations\n"]

    # Verify class exists
    if not hasattr(student_module, "CustomerManager"):
        error_msg = "ERROR: CustomerManager class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return
    test_cases = [
        {
            "desc": "Count customers in region North",
            "func": "count_customers_by_region",
            "setup": lambda: student_module.CustomerManager(),
            "call": lambda obj: obj.count_customers_by_region("North"),
            "check": lambda output: "Total Customers in North: 3" in output,
            "expected_output": "Should print 'Total Customers in North: 3'",
            "marks": 3
        },
        {
            "desc": "Find customer with highest balance",
            "func": "find_highest_balance_customer",
            "setup": lambda: student_module.CustomerManager(),
            "call": lambda obj: obj.find_highest_balance_customer(),
            "check": lambda output: "Highest Balance Customer: Deepa (C104) - 5000.25" in output,
            "expected_output": "Should print 'Highest Balance Customer: Deepa (C104) - 5000.25'",
            "marks": 3
        },
        {
            "desc": "Check customer existence by ID",
            "func": "check_customer",
            "setup": lambda: student_module.CustomerManager(),
            "call": lambda obj: obj.check_customer("C101"),
            "check": lambda output: "Customer C101: Tushar - Balance: 1500.50" in output,
            "expected_output": "Should print 'Customer C101: Tushar - Balance: 1500.50' for parameter C101",
            "marks": 4
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 3)
        max_score += marks
        
        try:
            # Verify method exists
            method_exists, error_msg = validate_method_exists(student_module.CustomerManager(), case["func"])
            if not method_exists:
                msg = f"FAIL TC{idx} [{case['desc']}]: {error_msg}"
                print(msg)
                report_lines.append(msg)
                continue

            obj = case["setup"]()

            # Capture stdout for methods that print
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            try:
                # Use the provided call lambda to handle arguments consistently
                case["call"](obj)
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            # Execute test check
            passed = case["check"](output)
            
            if passed:
                msg = f"PASS TC{idx} [{case['desc']}]"
                total_score += marks
            else:
                # Provide detailed mismatch error  
                msg = f"FAIL TC{idx} [{case['desc']}]\n"
                msg += f"  Expected: {case['expected_output']}\n"
                msg += f"  Got Output: {repr(output)}\n"
                msg += f"  Hint: Check your print statements in '{case['func']}' method"
            
            print(msg)
            report_lines.append(msg)
        
        except TypeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}\n]"
            msg += f"  Error Type: Argument Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: check_customer() requires a customer ID parameter (e.g., 'C101')"
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Review the method implementation. Check data structure and iteration logic"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
