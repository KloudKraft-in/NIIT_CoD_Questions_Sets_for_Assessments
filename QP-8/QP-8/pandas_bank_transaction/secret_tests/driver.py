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

    print("🧪 Running Tests for: Bank Transaction Analyzer\n")
    report_lines = ["🧪 Running Tests for: Bank Transaction Analyzer\n"]

    # Load student's solution module
    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    analyzer = student_module.BankTransactionAnalyzer()

    # Load real CSV path
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "bank_transactions.csv"))

    # Custom test DataFrame
    test_df = pd.DataFrame({
        "customer_id": [101, 102, 103, 101, 104, 105, 106],
        "type": ["credit", "debit", "credit", "debit", "credit", "credit", "debit"],
        "amount": [12000, 8000, 5000, 4000, 20000, 15000, 3000],
        "date": [
            "2023-05-01", "2023-05-02", "2023-05-03", "2023-05-04",
            "2023-05-05", "2023-05-06", "2023-05-07"
        ]
    })

    test_cases = [
        {
            "desc": "Load transactions CSV",
            "func": "load_transactions",
            "input": csv_path,
            "expected_type": pd.DataFrame,
            "marks": 5
        },
        {
            "desc": "Calculate total credit/debit",
            "func": "total_by_type",
            "input": test_df.copy(),
            "expected_value": {"credit": 52000.0, "debit": 15000.0},
            "marks": 5
        },
        {
            "desc": "Filter high-value transactions > 10000",
            "func": "high_value_transactions",
            "input": test_df.copy(),
            "expected_type": pd.DataFrame,
            "marks": 5
        },
        {
            "desc": "Find top 3 customers by total amount",
            "func": "top_customers",
            "input": test_df.copy(),
            "expected_value": [(104, 20000.0), (101, 16000.0), (105, 15000.0)],
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

            if 'pass' in src and len(src) < 80:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                print(msg)
                report_lines.append(msg)
                continue

            result = func(case["input"]) if isinstance(case["input"], (pd.DataFrame, str)) else func(*case["input"])

            if "expected_type" in case:
                passed = isinstance(result, case["expected_type"])
            elif isinstance(case["expected_value"], dict):
                expected = case["expected_value"]
                credit_ok = round(result.get("credit", 0), 2) == round(expected.get("credit", 0), 2)
                debit_ok = round(result.get("debit", 0), 2) == round(expected.get("debit", 0), 2)
                passed = credit_ok and debit_ok
            elif isinstance(case["expected_value"], list):
                passed = result == case["expected_value"]
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

    score_line = f"\n🎯 TOTAL SCORE: {total_score}/{max_score}"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
