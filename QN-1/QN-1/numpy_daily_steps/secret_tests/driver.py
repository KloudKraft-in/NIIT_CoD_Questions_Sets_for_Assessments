import importlib.util
import datetime
import os
import numpy as np

def test_student_code(solution_path):
    # Load student solution.py dynamically
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    # Create instance of the class
    tracker = student_module.DailyStepsTracker()

    # Initialize results log
    results = []
    results.append("🧪 Running Tests for: DailyStepsTracker\n")

    # Test Case 1: create_steps_array
    try:
        arr = tracker.create_steps_array([3000, 7000, 12000, 1500])
        if isinstance(arr, np.ndarray) and np.array_equal(arr, np.array([3000, 7000, 12000, 1500])):
            results.append("✅ Visible Test Case 1 Passed: Create steps array")
        else:
            results.append("❌ Visible Test Case 1 Failed: Create steps array")
    except Exception:
        results.append("❌ Visible Test Case 1 Failed: Create steps array")

    # Test Case 2: calculate_total_steps (independent test)
    try:
        total = tracker.calculate_total_steps(np.array([3000, 7000, 12000]))
        if total == 22000:
            results.append("✅ Visible Test Case 2 Passed: Calculate total steps")
        else:
            results.append("❌ Visible Test Case 2 Failed: Calculate total steps")
    except Exception:
        results.append("❌ Visible Test Case 2 Failed: Calculate total steps")

    # Test Case 3: calculate_average_steps (does NOT rely on total_steps)
    try:
        avg = tracker.calculate_average_steps(np.array([3000, 7000, 12000]))
        expected_avg = round((3000 + 7000 + 12000) / 3, 1)
        if avg == expected_avg:
            results.append("✅ Visible Test Case 3 Passed: Calculate average steps")
        else:
            results.append("❌ Visible Test Case 3 Failed: Calculate average steps")
    except Exception:
        results.append("❌ Visible Test Case 3 Failed: Calculate average steps")

    # Test Case 4: days_above_target
    try:
        result = tracker.days_above_target(np.array([5000, 8000, 10000, 3000]), 6000)
        expected = np.array([8000, 10000])
        if isinstance(result, np.ndarray) and np.array_equal(result, expected):
            results.append("✅ Visible Test Case 4 Passed: Days above target")
        else:
            results.append("❌ Visible Test Case 4 Failed: Days above target")
    except Exception:
        results.append("❌ Visible Test Case 4 Failed: Days above target")

    # Hidden Test Case 1: Handle empty input
    try:
        result = tracker.days_above_target(np.array([]), 5000)
        if isinstance(result, np.ndarray) and result.size == 0:
            results.append("✅ Hidden Test Case 1 Passed: Handle empty input")
        else:
            results.append("❌ Hidden Test Case 1 Failed: Handle empty input")
    except Exception:
        results.append("❌ Hidden Test Case 1 Failed: Handle empty input")

    # Generate report file with timestamp
    report_folder = os.path.join(os.path.dirname(solution_path), "..", "reports")
    os.makedirs(report_folder, exist_ok=True)
    existing_reports = [f for f in os.listdir(report_folder) if f.startswith("report") and f.endswith(".txt")]
    report_filename = f"report_{len(existing_reports) + 1}.txt"
    report_path = os.path.join(report_folder, report_filename)

    with open(report_path, "w", encoding="utf-8") as f:
        for line in results:
            print(line)
            f.write(line + "\n")