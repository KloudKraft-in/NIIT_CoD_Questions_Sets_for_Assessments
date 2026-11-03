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

    print("🧪 Running Tests for: HR Analytics System\n")
    report_lines = ["🧪 Running Tests for: HR Analytics System\n"]

    # Load solution
    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)
    analyzer = student_module.HRAnalytics()

    emp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "employees.csv"))
    att_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "attendance.csv"))

    emp_df = pd.DataFrame({
        "emp_id": ["E101", "E102", "E103", "E104", "E105"],
        "name": ["Alice", "Bob", "Charlie", "David", "Eva"],
        "department": ["HR", "IT", "Finance", "HR", "IT"]
    })

    att_df = pd.DataFrame({
        "emp_id": ["E101", "E101", "E102", "E103"],
        "login_time": pd.to_datetime(["2023-05-01 09:00", "2023-05-02 09:00", "2023-05-01 10:15", "2023-05-01 09:30"]),
        "logout_time": pd.to_datetime(["2023-05-01 17:00", "2023-05-02 17:00", "2023-05-01 18:00", "2023-05-01 17:30"])
    })

    test_cases = [
        {
            "desc": "Load both employee and attendance files",
            "func": "load_data",
            "input": (emp_path, att_path),
            "expected_type": tuple,
            "marks": 5
        },
        {
            "desc": "Calculate total working hours per employee",
            "func": "total_working_hours",
            "input": att_df.copy(),
            "expected_value": {"E101": 16.0, "E102": 7.75, "E103": 8.0},
            "marks": 5
        },
        {
            "desc": "Identify employees who logged in late",
            "func": "late_joiners",
            "input": att_df.copy(),
            "expected_value": ["E102"],
            "marks": 5
        },
        {
            "desc": "Find employees without attendance records",
            "func": "absentees",
            "input": (emp_df.copy(), att_df.copy()),
            "expected_value": ["E104", "E105"],
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 1)
        max_score += marks

        try:
            func = getattr(analyzer, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()

            if "pass" in src and len(src) < 80:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                print(msg)
                report_lines.append(msg)
                continue

            result = func(*case["input"]) if isinstance(case["input"], tuple) else func(case["input"])

            if "expected_type" in case:
                passed = isinstance(result, case["expected_type"])
            elif isinstance(case["expected_value"], dict):
                expected = case["expected_value"]
                passed = all(round(result.get(k, 0), 2) == round(v, 2) for k, v in expected.items())
            elif isinstance(case["expected_value"], list):
                passed = sorted(result) == sorted(case["expected_value"])
            else:
                passed = round(result, 2) == round(case["expected_value"], 2)

            if passed:
                total_score += marks
                msg = f"✅ Visible Test Case {idx} Passed: {case['desc']}"
            else:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"

        except Exception as e:
            msg = f"❌ Visible Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"

        print(msg)
        report_lines.append(msg)

    score_line = f"\n🎯 TOTAL SCORE: {int(total_score)}/{int(max_score)}"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
