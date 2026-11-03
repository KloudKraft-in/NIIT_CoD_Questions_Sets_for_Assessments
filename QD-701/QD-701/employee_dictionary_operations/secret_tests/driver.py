import importlib.util
import os
import sys
from io import StringIO

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    print("Running Tests for: Employee Dictionary Operations\n")
    report_lines = ["Running Tests for: Employee Dictionary Operations\n"]

    test_cases = [
        {
            "desc": "Calculate average IT department salary",
            "func": "calculate_average_it_salary",
            "setup": lambda: student_module.EmployeeManager(),
            "call": lambda obj: obj.calculate_average_it_salary(),
            "check": lambda output: "Average IT Salary: 55000.0" in output,
            "marks": 3
        },
        {
            "desc": "Find highest paid employee",
            "func": "find_highest_paid_employee",
            "setup": lambda: student_module.EmployeeManager(),
            "call": lambda obj: obj.find_highest_paid_employee(),
            "check": lambda output: "Highest Paid Employee: Vikram (E005) - 60000" in output,
            "marks": 3
        },
        {
            "desc": "Check employee existence by ID",
            "func": "check_employee",
            "setup": lambda: student_module.EmployeeManager(),
            "call": lambda obj: obj.check_employee("E002"),
            "check": lambda output: "Employee E002: Priya - 45000" in output,
            "marks": 4
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 3)
        is_hidden = case.get("is_hidden", False)
        
        if not is_hidden:
            max_score += marks
        
        try:
            obj = case["setup"]()
            
            # Capture stdout for methods that print
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                # Special handling for check_employee with parameter
                if case["func"] == "check_employee":
                    obj.check_employee("E002")
                else:
                    getattr(obj, case["func"])()
                
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            # Execute test check
            passed = case["check"](output)
            
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

    score_line = f"\nSCORE: {total_score}/10.0 (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
