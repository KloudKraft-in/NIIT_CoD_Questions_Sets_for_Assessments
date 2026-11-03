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
    spec.loader.exec_module(student_module)

    analyzer = student_module.ClaimsAnalyzer()

    print("🧪 Running Tests for: Insurance Claim Processing Analysis\n")
    report_lines = ["🧪 Running Tests for: Insurance Claim Processing Analysis\n"]

    # Define test DataFrames for reuse across independent tests
    test_df_1 = pd.DataFrame({
        "CustomerID": [1001, 1002],
        "Category": ["Health", "Auto"],
        "Amount": [5000.0, 2000.0],
        "Status": ["Approved", "Rejected"],
        "Date": ["2024-05-01", "2024-05-01"]
    })

    test_df_2 = pd.DataFrame({
        "CustomerID": [1001, 1002, 1003, 1004],
        "Category": ["Health", "Health", "Auto", "Auto"],
        "Amount": [5000.0, 3000.0, 2000.0, 4000.0],
        "Status": ["Approved", "Approved", "Rejected", "Approved"],
        "Date": ["2024-05-01", "2024-05-01", "2024-05-01", "2024-05-01"]
    })

    test_df_3 = pd.DataFrame({
        "CustomerID": [1001, 1002, 1003],
        "Category": ["Health", "Auto", "Home"],
        "Amount": [5000.0, 2000.0, 8000.0],
        "Status": ["Approved", "Rejected", "Pending"],
        "Date": ["2024-05-01", "2024-05-01", "2024-05-01"]
    })

    test_df_4 = pd.DataFrame({
        "CustomerID": [1001, 1002, 1003],
        "Category": ["Health", "Auto", "Home"],
        "Amount": [5000.0, 2000.0, 8000.0],
        "Status": ["Pending", "Pending", "Approved"],
        "Date": ["2024-05-01", "2024-05-01", "2024-05-01"]
    })

    test_df_5 = pd.DataFrame({
        "CustomerID": [1001, 1002, 1003],
        "Category": ["Health", "Auto", "Home"],
        "Amount": [5000.0, 2000.0, 8000.0],
        "Status": ["Approved", "Rejected", "Pending"],
        "Date": ["2024-05-01", "2024-05-01", "2024-05-01"]
    })

    # Hidden test DataFrames
    test_df_invalid = pd.DataFrame({
        "CustomerID": [1001, 1002, 1003, 1004],
        "Category": ["Health", "Auto", "Home", "Life"],
        "Amount": [5000.0, 2000.0, -500.0, 3000.0],
        "Status": ["Approved", "Invalid", "Pending", "Approved"],
        "Date": ["2024-05-01", "2024-05-01", "2024-05-01", "2024-05-01"]
    })

    test_df_negative = pd.DataFrame({
        "CustomerID": [1001, 1002, 1003],
        "Category": ["Health", "Auto", "Home"],
        "Amount": [5000.0, -2000.0, 8000.0],
        "Status": ["Approved", "Approved", "Pending"],
        "Date": ["2024-05-01", "2024-05-01", "2024-05-01"]
    })

    test_df_tie_pending = pd.DataFrame({
        "CustomerID": [1001, 1002, 1003],
        "Category": ["Health", "Auto", "Home"],
        "Amount": [5000.0, 5000.0, 3000.0],
        "Status": ["Pending", "Pending", "Approved"],
        "Date": ["2024-05-01", "2024-05-01", "2024-05-01"]
    })

    test_cases = [
        {
            "desc": "Create structured claims DataFrame",
            "func": "create_claims_df",
            "input": [[1001, "Health", 5000.0, "Approved", "2024-05-01"]],
            "expected_type": pd.DataFrame,
            "marks": 2.5
        },
        {
            "desc": "Approval rate by category",
            "func": "approval_rate_by_category",
            "input": test_df_2.copy(),
            "expected_columns": ["Category", "Approval Rate"],
            "marks": 2.5
        },
        {
            "desc": "Flag high-value claims",
            "func": "add_flag_high_amount",
            "input": (test_df_1.copy(), 3000.0),
            "expected_columns": ["IsHighValue"],
            "marks": 2.5
        },
        {
            "desc": "Get top N pending claims",
            "func": "get_top_pending_claims",
            "input": (test_df_4.copy(), 2),
            "expected_type": pd.DataFrame,
            "marks": 2.5
        },
        {
            "desc": "Claim summary by status",
            "func": "claim_summary_by_status",
            "input": test_df_5.copy(),
            "expected_columns": ["Status", "TotalAmount", "MinAmount", "MaxAmount", "AvgAmount"],
            "marks": 2.5
        },
        {
            "desc": "Remove invalid claims (invalid Status)",
            "func": "clean_invalid_claims",
            "input": test_df_invalid.copy(),
            "expected_rows": 2,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Handle missing/negative amounts",
            "func": "clean_invalid_claims",
            "input": test_df_negative.copy(),
            "expected_rows": 2,
            "marks": 2.5,
            "is_hidden": True
        },
        {
            "desc": "Tie in top pending claim amounts",
            "func": "get_top_pending_claims",
            "input": (test_df_tie_pending.copy(), 2),
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
        
        # Only count visible tests toward score
        if not is_hidden:
            max_score += marks
        
        try:
            func = getattr(analyzer, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()

            # Check 1: Pass-only
            if 'pass' in src and len(src) < 80:
                test_type = "🔒 Hidden" if is_hidden else "✅ Visible"
                msg = f"❌ {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue

            # Execute test
            if isinstance(case["input"], tuple):
                result = func(*case["input"])
            elif isinstance(case["input"], list):
                result = func(case["input"])
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
                test_type = "🔒 Hidden" if is_hidden else "✅ Visible"
                msg = f"{test_type} Test Case {idx} Passed: {case['desc']}"
                # Only add to score if visible
                if not is_hidden:
                    total_score += marks
            else:
                test_type = "🔒 Hidden" if is_hidden else "❌ Visible"
                msg = f"{test_type} Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"

        except Exception as e:
            test_type = "🔒 Hidden" if is_hidden else "❌ Visible"
            msg = f"{test_type} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"

        print(msg)
        report_lines.append(msg)

    # Print total score summary
    score_line = f"\n🎯 SCORE: {total_score}/12.5 (Visible) | Total: 20 (Visible: 12.5 + Hidden: 7.5)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
