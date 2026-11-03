import importlib.util
import os
import inspect

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    print("Running Tests for: Student Grade System\n")
    report_lines = ["Running Tests for: Student Grade System\n"]

    test_cases = [
        {
            "desc": "Register Alice (90.5) and verify info",
            "func": "add_student",
            "setup": lambda: (lambda obj: (obj.add_student("S101", "Alice", 90.5), obj)[-1])(student_module.GradeSystem()),
            "call": lambda obj: obj.get_student_info("S101"),
            "check": lambda result: isinstance(result, str) and result == "Name: Alice, Grade: 90.5",
            "marks": 2
        },
        {
            "desc": "Update Alice's grade to 95.0 and verify",
            "func": "update_grade",
            "setup": lambda: (lambda obj: (obj.add_student("S101", "Alice", 90.5), obj.update_grade("S101", 95.0), obj)[-1])(student_module.GradeSystem()),
            "call": lambda obj: obj.get_student_info("S101"),
            "check": lambda result: isinstance(result, str) and result == "Name: Alice, Grade: 95.0",
            "marks": 2
        },
        {
            "desc": "Add Bob (85.0) and verify class average",
            "func": "get_average",
            "setup": lambda: (lambda obj: (obj.add_student("S101", "Alice", 95.0), obj.add_student("S102", "Bob", 85.0), obj)[-1])(student_module.GradeSystem()),
            "call": lambda obj: obj.get_average(),
            "check": lambda result: isinstance(result, float) and result == 90.0,
            "marks": 2
        },
        {
            "desc": "Lookup non-existent student roll number",
            "func": "get_student_info",
            "setup": lambda: (lambda obj: (obj.add_student("S101", "Alice", 90.5), obj)[-1])(student_module.GradeSystem()),
            "call": lambda obj: obj.get_student_info("S999"),
            "check": lambda result: isinstance(result, str) and result == "Student Not Found",
            "marks": 2
        },
        {
            "desc": "Remove student and check average change",
            "func": "remove_student",
            "setup": lambda: (lambda obj: (obj.add_student("S101", "Alice", 95.0), obj.add_student("S102", "Bob", 85.0), obj.remove_student("S101"), obj)[-1])(student_module.GradeSystem()),
            "call": lambda obj: obj.get_average(),
            "check": lambda result: isinstance(result, float) and result == 85.0,
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

    score_line = f"\nSCORE: {total_score}/10.0 (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
