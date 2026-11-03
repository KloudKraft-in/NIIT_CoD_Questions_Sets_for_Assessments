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

    print("Running Tests for: Student Score List Analyzer\n")
    report_lines = ["Running Tests for: Student Score List Analyzer\n"]

    test_cases = [
        {
            "desc": "Create status dictionary mapping scores to Pass/Fail",
            "func": "create_status_dict",
            "setup": lambda: student_module.ScoreManager(),
            "call": lambda obj: obj.create_status_dict(),
            "check": lambda result: isinstance(result, dict) and result.get(92) == "Pass" and result.get(45) == "Fail",
            "marks": 2.5
        },
        {
            "desc": "Find highest score from list",
            "func": "find_highest_score",
            "setup": lambda: student_module.ScoreManager(),
            "call": lambda obj: obj.find_highest_score(),
            "check": lambda result: result == 95,
            "marks": 2.5
        },
        {
            "desc": "Calculate average score",
            "func": "calculate_average",
            "setup": lambda: student_module.ScoreManager(),
            "call": lambda obj: obj.calculate_average(),
            "check": lambda result: result == 71.5,
            "marks": 2.5
        },
        {
            "desc": "Get passing scores in descending order",
            "func": "get_passing_scores",
            "setup": lambda: student_module.ScoreManager(),
            "call": lambda obj: obj.get_passing_scores(),
            "check": lambda result: isinstance(result, list) and result == [95, 92, 88],
            "marks": 2.5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2.5)
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
