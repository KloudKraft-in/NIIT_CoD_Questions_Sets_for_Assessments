# secret_tests/driver.py

import importlib.util
import datetime
import os
import pandas as pd
import inspect

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    print("🧪 Running Tests for: Student Performance Tracker\n")
    report_lines = ["🧪 Running Tests for: Student Performance Tracker\n"]

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)
    tracker = student_module.StudentPerformanceTracker()

    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "student_scores.csv"))

    test_df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Math": [95, 80, 60, 72, 85],
        "Science": [92, 70, 85, 66, 88],
        "English": [100, 65, 75, 78, 90]
    })

    test_cases = [
        {
            "desc": "Load student marks CSV",
            "func": "load_student_data",
            "input": csv_path,
            "expected_type": pd.DataFrame,
            "marks": 5
        },
        {
            "desc": "Filter top scorers",
            "func": "get_top_scorers",
            "input": test_df.copy(),
            "expected_value": test_df.loc[[0]],  # Only Alice has scores > 90 in all
            "marks": 5
        },
        {
            "desc": "Calculate subject-wise averages",
            "func": "average_scores",
            "input": test_df.copy(),
            "expected_value": {
                "Math": 78.4,
                "Science": 80.2,
                "English": 81.6
            },
            "marks": 5
        },
        {
            "desc": "Return top 3 students by total score",
            "func": "top_students",
            "input": test_df.copy(),
            "expected_value": [("Alice", 287), ("Eve", 263), ("Charlie", 220)],
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case["marks"]
        max_score += marks

        try:
            func = getattr(tracker, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()

            if "pass" in src and len(src) < 80:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue

            result = func(case["input"]) if not isinstance(case["input"], tuple) else func(*case["input"])

            if "expected_type" in case:
                passed = isinstance(result, case["expected_type"])
            elif isinstance(case["expected_value"], pd.DataFrame):
                passed = result.reset_index(drop=True).equals(case["expected_value"].reset_index(drop=True))
            elif isinstance(case["expected_value"], dict):
                passed = all(round(result.get(k, 0), 2) == round(v, 2) for k, v in case["expected_value"].items())
            else:
                passed = result == case["expected_value"]

            if passed:
                total_score += marks
                msg = f"✅ Visible Test Case {idx} Passed: {case['desc']}"
            else:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"

        except Exception as e:
            msg = f"❌ Visible Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"

        print(msg)
        report_lines.append(msg)

    score_line = f"\n🎯 TOTAL SCORE: {total_score}/{max_score}"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
