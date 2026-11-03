# secret_tests/driver.py

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

    analyzer = student_module.RetailSalesAnalyzer()

    print("🧪 Running Tests for: Retail Sales Analysis\n")
    report_lines = ["🧪 Running Tests for: Retail Sales Analysis\n"]

    # ✅ Use absolute path to CSV from data folder
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "sales_sample.csv"))

    # Define a known test DataFrame (for testing other cases)
    test_df = pd.DataFrame({
        "product_name": ["Rice", "Notebook", "Soap", "Soap", "Rice", "Notebook"],
        "product_category": ["Grocery", "Stationery", "Personal Care", "Personal Care", "Grocery", "Stationery"],
        "quantity": [200, 210, 190, 200, 230, 210],
        "unit_price": [50.0, 30.0, 20.0, 20.0, 50.0, 30.0]
    })

    test_cases = [
        {
            "desc": "Load CSV into DataFrame",
            "func": "load_transactions",
            "input": csv_path,
            "expected_type": pd.DataFrame,
            "marks": 5
        },
        {
            "desc": "Calculate total purchase value",
            "func": "total_purchase_value",
            "input": test_df.copy(),
            "expected_value": 41900.0,
            "marks": 5
        },
        {
            "desc": "Find top product category",
            "func": "top_product_category",
            "input": test_df.copy(),
            "expected_value": ("Grocery", 21500.0),
            "marks": 5
        },
        {
            "desc": "Get top 3 products by quantity sold",
            "func": "top_n_products",
            "input": test_df.copy(),
            "expected_value": [("Rice", 430), ("Notebook", 420), ("Soap", 390)],
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 5)
        max_score += marks
        try:
            func = getattr(analyzer, case["func"])
            src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()

            # Check 1: Pass-only
            if 'pass' in src and len(src) < 80:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue

            # Execute test
            result = func(case["input"]) if isinstance(case["input"], (pd.DataFrame, str)) else func(*case["input"])

            # Evaluate result
            if "expected_type" in case:
                passed = isinstance(result, case["expected_type"])
            elif isinstance(case["expected_value"], list):
                passed = result == case["expected_value"]
            elif isinstance(case["expected_value"], tuple):
                passed = (
                    result[0] == case["expected_value"][0] and
                    round(result[1], 2) == round(case["expected_value"][1], 2)
                )
            else:
                passed = round(result, 2) == round(case["expected_value"], 2)

            if passed:
                msg = f"✅ Visible Test Case {idx} Passed: {case['desc']}"
                total_score += marks
            else:
                msg = f"❌ Visible Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"

        except Exception as e:
            msg = f"❌ Visible Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"

        print(msg)
        report_lines.append(msg)

    # Print total score summary
    score_line = f"\n🎯 TOTAL SCORE: {total_score}/{max_score}"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
