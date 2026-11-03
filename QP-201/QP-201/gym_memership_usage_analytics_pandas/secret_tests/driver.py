import importlib.util
import datetime
import os
import pandas as pd
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

    print("🧪 Running Tests for: Gym Membership Usage Analytics (Strict Independence Mode)\n")
    report_lines = ["🧪 Running Tests for: Gym Membership Usage Analytics (Strict Independence Mode)\n"]

    # Define test DataFrames for reuse across independent tests
    test_df_1 = pd.DataFrame({
        "Member": ["Alice", "Bob"],
        "Branch": ["Downtown", "Uptown"],
        "Workout": ["Cardio", "Weights"],
        "Duration": [45, 60]
    })

    test_df_2 = pd.DataFrame({
        "Member": ["Alice", "Alice", "Bob"],
        "Branch": ["Downtown", "Downtown", "Uptown"],
        "Workout": ["Cardio", "Yoga", "Weights"],
        "Duration": [45, 30, 60]
    })

    test_df_4 = pd.DataFrame({
        "Member": ["Alice", "Bob", "Zoe"],
        "Branch": ["A", "B", "C"],
        "Workout": ["Yoga", "Cardio", "Weights"],
        "Duration": [30, 60, 45],
        "Calories Burned": [150, 480, 315]
    })

    # Hidden test DataFrames
    test_df_duplicates = pd.DataFrame({
        "Member": ["Alice", "Bob", "Alice"],
        "Branch": ["Downtown", "Uptown", "Downtown"],
        "Workout": ["Cardio", "Weights", "Cardio"],
        "Duration": [45, 60, 45]
    })

    test_df_zero_duration = pd.DataFrame({
        "Member": ["Alice", "Bob", "Zoe"],
        "Branch": ["A", "B", "C"],
        "Workout": ["Cardio", "Weights", "Yoga"],
        "Duration": [0, 60, 45]
    })

    test_df_tie_top = pd.DataFrame({
        "Member": ["Alice", "Bob", "Zoe"],
        "Branch": ["A", "B", "C"],
        "Workout": ["Cardio", "Cardio", "Yoga"],
        "Duration": [60, 60, 45],
        "Calories Burned": [480, 480, 225]
    })

    test_cases = [
        {
            "desc": "Create usage DataFrame from raw data",
            "func": "create_usage_df",
            "input": [["Alice", "Downtown", "Cardio", 45]],
            "expected_type": pd.DataFrame,
            "marks": 2.5
        },
        {
            "desc": "Compute total duration per member",
            "func": "compute_total_duration",
            "input": test_df_2,
            "expected_columns": ["Total Duration"],
            "marks": 2.5
        },
        {
            "desc": "Add calorie column to DataFrame",
            "func": "add_calorie_column",
            "input": test_df_1,
            "expected_columns": ["Calories Burned"],
            "marks": 2.5
        },
        {
            "desc": "Filter sessions longer than threshold",
            "func": "filter_long_sessions",
            "input": (test_df_1, 45),
            "expected_rows": 2,
            "marks": 2.5
        },
        {
            "desc": "Get top N sessions by calories",
            "func": "get_top_sessions",
            "input": (test_df_4, 2),
            "expected_type": pd.DataFrame,
            "marks": 2.5
        },
        {
            "desc": "Remove duplicate logs",
            "func": "remove_duplicates",
            "input": test_df_duplicates,
            "expected_rows": 2,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Handle zero duration session",
            "func": "compute_total_duration",
            "input": test_df_zero_duration,
            "expected_columns": ["Total Duration"],
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Handle tie in top calorie-burning sessions",
            "func": "get_top_sessions",
            "input": (test_df_tie_top, 2),
            "expected_type": pd.DataFrame,
            "marks": 2.5,
            "is_hidden": True
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
            # CREATE FRESH OBJECT FOR EVERY TEST CASE (Strict Independence)
            analyzer = student_module.GymUsageAnalyzer()
            
            if not hasattr(analyzer, case["func"]):
                msg = f" Test Case {idx} Failed: Method '{case['func']}' not found"
                print(msg)
                report_lines.append(msg)
                continue

            func = getattr(analyzer, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()

            # Check for pass-only implementation
            if 'pass' in src and len(src) < 80:
                test_type = " Hidden" if is_hidden else " Visible"
                msg = f" {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue

            # Prepare Input (Always using FRESH COPIES from driver data)
            if isinstance(case["input"], tuple):
                input_data = tuple(item.copy() if isinstance(item, pd.DataFrame) else item for item in case["input"])
                result = func(*input_data)
            elif isinstance(case["input"], pd.DataFrame):
                result = func(case["input"].copy())
            elif isinstance(case["input"], list):
                result = func(case["input"][:]) # Shallow copy of list
            else:
                result = func(case["input"])

            # Evaluate result
            passed = False
            if "expected_type" in case:
                passed = isinstance(result, case["expected_type"])
            elif "expected_columns" in case:
                passed = all(col in result.columns for col in case["expected_columns"])
            elif "expected_rows" in case:
                passed = result.shape[0] == case["expected_rows"]
            
            if passed:
                test_type = " Hidden" if is_hidden else " Visible"
                msg = f"{test_type} Test Case {idx} Passed: {case['desc']}"
                if not is_hidden:
                    total_score += marks
            else:
                test_type = " Hidden" if is_hidden else " Visible"
                msg = f"{test_type} Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"

        except Exception as e:
            test_type = " Hidden" if is_hidden else " Visible"
            msg = f"{test_type} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"

        print(msg)
        report_lines.append(msg)

    score_line = f"\n SCORE: {total_score}/{max_score} (Visible) | Total Max: 20 (Visible: 12.5 + Hidden: 7.5)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
