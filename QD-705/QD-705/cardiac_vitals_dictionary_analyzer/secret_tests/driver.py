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

    print("Running Tests for: Cardiac Vitals Dictionary Analyzer\n")
    report_lines = ["Running Tests for: Cardiac Vitals Dictionary Analyzer\n"]

    # Verify class exists
    if not hasattr(student_module, "HealthMonitor"):
        error_msg = "ERROR: HealthMonitor class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    test_cases = [
        {
            "desc": "Initial State",
            "func": "__init__",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: print(str(obj.records)),
            "check": lambda output: "'PatientID': 'P01'" in output and "'HeartRate': 72" in output and "'HeartRate': None" in output,
            "expected_output": "Should initialize self.records with default records dict",
            "marks": 0
        },
        {
            "desc": "Clean Records",
            "func": "clean_records",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.clean_records(),
            "check": lambda output: "Removed Records: 2" in output,
            "expected_output": "Should print 'Removed Records: 2'",
            "marks": 4
        },
        {
            "desc": "Find Highest Rate",
            "func": "find_highest_rate",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.find_highest_rate(),
            "check": lambda output: "Highest Heart Rate: 110" in output,
            "expected_output": "Should print 'Highest Heart Rate: 110'",
            "marks": 4
        },
        {
            "desc": "Patient Averages",
            "func": "patient_averages",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.patient_averages(),
            "check": lambda output: "P01: 72.33" in output and "P02: 85.00" in output and "P03: 107.50" in output and "P04: 71.50" in output and "P05: 85.00" in output,
            "expected_output": "Should print sorted list of Patient averages: P01: 72.33, etc.",
            "marks": 4
        },
        {
            "desc": "High Risk Identification",
            "func": "high_risk",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.high_risk(100),
            "check": lambda output: "High Risk Patients: P03" in output,
            "expected_output": "Should print 'High Risk Patients: P03' for parameter 100",
            "marks": 4
        },
        {
            "desc": "Count High Risk Patients",
            "func": "count_high_risk",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.count_high_risk(100),
            "check": lambda output: "High Risk Patient Count: 1" in output,
            "expected_output": "Should print 'High Risk Patient Count: 1' for parameter 100",
            "marks": 4
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 4)
        max_score += marks
        
        try:
            # Verify method exists (except init)
            if case["func"] != "__init__":
                method_exists, error_msg = validate_method_exists(student_module.HealthMonitor(), case["func"])
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
            msg += f"  Hint: check the number of parameters required by '{case['func']}' method"
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
