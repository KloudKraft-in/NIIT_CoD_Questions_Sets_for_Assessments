import importlib.util
import os
import inspect

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(student_module)
    except Exception as e:
        print(f"IMPORT ERROR: {e}")
        return

    print("Running Tests for: Student Result Registry\n")
    report_lines = ["Running Tests for: Student Result Registry\n"]

    # Sample input to use for strict independence
    sample_scores = [45, 78, 92, 55, 88, 67, 95, 52]

    def run_independent_test(obj, func_name, scores):
        """Force input scores onto the object before calling the function."""
        obj.scores = scores
        return getattr(obj, func_name)()

    test_cases = [
        {
            "desc": "Verify pass/fail dictionary mapping",
            "func": "create_status_dict",
            "setup": lambda: student_module.ResultRegistry(),
            "call": lambda obj: run_independent_test(obj, "create_status_dict", sample_scores),
            "check": lambda result: isinstance(result, dict) and result.get(92) == "Pass" and result.get(45) == "Fail" and len(result) == 8,
            "marks": 5.0
        },
        {
            "desc": "Verify identification of the highest score",
            "func": "find_highest_score",
            "setup": lambda: student_module.ResultRegistry(),
            "call": lambda obj: run_independent_test(obj, "find_highest_score", sample_scores),
            "check": lambda result: result == 95,
            "marks": 5.0
        },
        {
            "desc": "Verify average calculation and rounding",
            "func": "calculate_average",
            "setup": lambda: student_module.ResultRegistry(),
            "call": lambda obj: run_independent_test(obj, "calculate_average", sample_scores),
            "check": lambda result: result == 71.5,
            "marks": 5.0
        },
        {
            "desc": "Verify sorted descending passing scores",
            "func": "get_passing_scores",
            "setup": lambda: student_module.ResultRegistry(),
            "call": lambda obj: run_independent_test(obj, "get_passing_scores", sample_scores),
            "check": lambda result: isinstance(result, list) and result == [95, 92, 88],
            "marks": 5.0
        },
        {
            "desc": "Verify sorted ascending failed scores",
            "func": "get_failed_scores",
            "setup": lambda: student_module.ResultRegistry(),
            "call": lambda obj: run_independent_test(obj, "get_failed_scores", sample_scores),
            "check": lambda result: isinstance(result, list) and result == [45, 52, 55, 67, 78],
            "marks": 5.0
        },
        {
            "desc": "Verify outcome frequency count dictionary",
            "func": "count_pass_fail",
            "setup": lambda: student_module.ResultRegistry(),
            "call": lambda obj: run_independent_test(obj, "count_pass_fail", sample_scores),
            "check": lambda result: isinstance(result, dict) and result.get('Pass') == 3 and result.get('Fail') == 5,
            "marks": 5.0
        }
    ]

    total_score = 0
    max_score = 30.0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 5.0)
        
        try:
            # Check if class exists
            if not hasattr(student_module, "ResultRegistry"):
                msg = f"FAIL TC{idx} Failed: ResultRegistry class missing"
                print(msg)
                report_lines.append(msg)
                continue

            obj = case["setup"]()
            
            # Check for method exists
            if not hasattr(obj, case["func"]):
                msg = f"FAIL TC{idx} Failed: {case['desc']} | Reason: Method '{case['func']}' missing"
                print(msg)
                report_lines.append(msg)
                continue

            # Execute test
            result = case["call"](obj)
            passed = case["check"](result)
            
            if passed:
                msg = f"PASS TC{idx} Passed: {case['desc']} ({marks}/5.0)"
                total_score += marks
            else:
                msg = f"FAIL TC{idx} Failed: {case['desc']} | Reason: Output mismatch"
            
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} Crashed: {case['desc']} | Error: {str(e)}"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/{max_score}"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
