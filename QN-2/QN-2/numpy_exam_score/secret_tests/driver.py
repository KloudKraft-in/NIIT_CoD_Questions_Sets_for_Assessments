import importlib.util
import os
import numpy as np

def test_student_code(solution_path):
    # Load student solution.py dynamically
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    # Create instance of the class
    analyzer = student_module.ExamScoreAnalyzer()

    # Initialize results log
    results = []
    results.append("🧪 Running Tests for: ExamScoreAnalyzer\n")

    # Test Case 1: load_scores
    try:
        analyzer.load_scores([45, 67, 89, 34])
        if np.array_equal(analyzer.scores, np.array([45, 67, 89, 34])):
            results.append("✅ Visible Test Case 1 Passed: load_scores() works with input [45, 67, 89, 34]")
        else:
            results.append("❌ Visible Test Case 1 Failed: load_scores() did not load correctly")
    except Exception:
        results.append("❌ Visible Test Case 1 Failed: Exception in load_scores()")

    # Test Case 2: compute_summary
    try:
        analyzer.load_scores([50, 80, 90])
        summary = analyzer.compute_summary()
        if summary == "Average: 73.3, Max: 90, Min: 50":
            results.append("✅ Visible Test Case 2 Passed: compute_summary() returned correct summary")
        else:
            results.append("❌ Visible Test Case 2 Failed: compute_summary() incorrect")
    except Exception:
        results.append("❌ Visible Test Case 2 Failed: Exception in compute_summary()")

    # Test Case 3: get_passing_scores
    try:
        analyzer.load_scores([30, 40, 60, 20, 75])
        passing = analyzer.get_passing_scores()
        expected = np.array([40, 60, 75])
        if isinstance(passing, np.ndarray) and np.array_equal(passing, expected):
            results.append("✅ Visible Test Case 3 Passed: get_passing_scores() returned correct values")
        else:
            results.append("❌ Visible Test Case 3 Failed: get_passing_scores() incorrect")
    except Exception:
        results.append("❌ Visible Test Case 3 Failed: Exception in get_passing_scores()")

    # Hidden Test Case 1: assign_grades logic
    try:
        analyzer.load_scores([95, 76, 61, 41, 30])
        grades = analyzer.assign_grades()
        expected = ['A', 'B', 'C', 'D', 'F']
        if grades == expected:
            results.append("✅ Hidden Test Case 1 Passed: assign_grades() returned correct grades")
        else:
            results.append("❌ Hidden Test Case 1 Failed: assign_grades() incorrect")
    except Exception:
        results.append("❌ Hidden Test Case 1 Failed: Exception in assign_grades()")

    # Hidden Test Case 2: assign_grades handles failing scores
    try:
        analyzer.load_scores([10, 20, 30])
        grades = analyzer.assign_grades()
        if grades == ['F', 'F', 'F']:
            results.append("✅ Hidden Test Case 2 Passed: assign_grades() handles failing scores")
        else:
            results.append("❌ Hidden Test Case 2 Failed: assign_grades() incorrect for low scores")
    except Exception:
        results.append("❌ Hidden Test Case 2 Failed: Exception in assign_grades()")

    # Save report to ../reports/report_X.txt
    report_folder = os.path.join(os.path.dirname(solution_path), "..", "reports")
    os.makedirs(report_folder, exist_ok=True)
    existing_reports = [f for f in os.listdir(report_folder) if f.startswith("report") and f.endswith(".txt")]
    report_filename = f"report_{len(existing_reports) + 1}.txt"
    report_path = os.path.join(report_folder, report_filename)

    with open(report_path, "w", encoding="utf-8") as f:
        for line in results:
            print(line)         # ✅ Show in terminal
            f.write(line + "\n")
