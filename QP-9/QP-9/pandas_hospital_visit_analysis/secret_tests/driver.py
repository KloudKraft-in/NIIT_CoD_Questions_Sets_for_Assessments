# 📁 secret_tests/driver.py
import importlib.util
import os
import pandas as pd

def test_student_code(solution_path):
    # Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base_dir, "..", "data"))
    report_dir = os.path.abspath(os.path.join(base_dir, "..", "reports"))
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "report.txt")

    # Load student module
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)
    analyzer = student_module.HospitalAnalysis()

    # Prepare input DataFrames
    patients_df = pd.read_csv(os.path.join(data_dir, "patients.csv"))
    visits_df = pd.read_csv(os.path.join(data_dir, "visits.csv"))

    results = []
    results.append("🧪 Running Tests for: Hospital Analysis\n")
    total_score = 0

    # Test 1: Load patients CSV
    try:
        df = analyzer.load_patients(os.path.join(data_dir, "patients.csv"))
        if isinstance(df, pd.DataFrame) and not df.empty:
            results.append("✅ Test Case 1 Passed: load_patients()")
            total_score += 2
        else:
            results.append("❌ Test Case 1 Failed: load_patients() - Output mismatch or empty")
    except Exception as e:
        results.append(f"❌ Test Case 1 Crashed: load_patients() - Error: {e}")

    # Test 2: Load visits CSV
    try:
        df = analyzer.load_visits(os.path.join(data_dir, "visits.csv"))
        if isinstance(df, pd.DataFrame) and not df.empty:
            results.append("✅ Test Case 2 Passed: load_visits()")
            total_score += 3
        else:
            results.append("❌ Test Case 2 Failed: load_visits() - Output mismatch or empty")
    except Exception as e:
        results.append(f"❌ Test Case 2 Crashed: load_visits() - Error: {e}")

    # Test 3: Merge DataFrames
    try:
        merged = analyzer.merge_dataframes(patients_df, visits_df)
        if isinstance(merged, pd.DataFrame) and 'visit_id' in merged.columns:
            results.append("✅ Test Case 3 Passed: merge_dataframes()")
            total_score += 3
        else:
            results.append("❌ Test Case 3 Failed: merge_dataframes() - Missing or invalid result")
    except Exception as e:
        results.append(f"❌ Test Case 3 Crashed: merge_dataframes() - Error: {e}")

    # Test 4: Patient with Most Visits
    try:
        merged = analyzer.merge_dataframes(patients_df, visits_df)
        result = analyzer.patient_with_most_visits(merged)
        if isinstance(result, tuple) and isinstance(result[1], int):
            results.append("✅ Test Case 4 Passed: patient_with_most_visits()")
            total_score += 3
        else:
            results.append("❌ Test Case 4 Failed: patient_with_most_visits() - Output format incorrect")
    except Exception as e:
        results.append(f"❌ Test Case 4 Crashed: patient_with_most_visits() - Error: {e}")

    # Test 5: Longest Visit
    try:
        result = analyzer.longest_visit_id(visits_df)
        if isinstance(result, int):
            results.append("✅ Test Case 5 Passed: longest_visit_id()")
            total_score += 3
        else:
            results.append("❌ Test Case 5 Failed: longest_visit_id() - Output should be int")
    except Exception as e:
        results.append(f"❌ Test Case 5 Crashed: longest_visit_id() - Error: {e}")

    # Test 6: Patient with No Visits
    try:
        result = analyzer.patients_with_no_visits(patients_df, visits_df)
        if isinstance(result, list):
            results.append("✅ Test Case 6 Passed: patients_with_no_visits()")
            total_score += 3
        else:
            results.append("❌ Test Case 6 Failed: patients_with_no_visits() - Expected a list")
    except Exception as e:
        results.append(f"❌ Test Case 6 Crashed: patients_with_no_visits() - Error: {e}")

    # Test 7: Average Visit Duration
    try:
        result = analyzer.average_visit_duration(visits_df)
        if isinstance(result, float):
            results.append("✅ Test Case 7 Passed: average_visit_duration()")
            total_score += 3
        else:
            results.append("❌ Test Case 7 Failed: average_visit_duration() - Output should be float")
    except Exception as e:
        results.append(f"❌ Test Case 7 Crashed: average_visit_duration() - Error: {e}")

    results.append(f"\n🎯 TOTAL SCORE: {total_score}/20")

    with open(report_path, "w", encoding="utf-8") as f:
        for line in results:
            print(line)
            f.write(line + "\n")

if __name__ == "__main__":
    student_solution_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py"))
    test_student_code(student_solution_path)
