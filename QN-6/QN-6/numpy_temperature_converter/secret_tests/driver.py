import importlib.util
import os
from datetime import datetime
import numpy as np

def test_student_code(solution_path):
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solution)

    results = []
    results.append("🧪 Running Tests for: temperature_converter")

    # VISIBLE TEST CASES
    try:
        result = solution.create_temperature_array([10, 20, 30])
        if isinstance(result, np.ndarray):
            results.append("✅ Visible Test Case 1 Passed: Create temperature array")
        else:
            results.append("❌ Visible Test Case 1 Failed: Create temperature array")
    except Exception as e:
        results.append(f"❌ Visible Test Case 1 Failed: Create temperature array ({e})")

    try:
        result = solution.convert_to_fahrenheit(np.array([0, 100]))
        if isinstance(result, np.ndarray):
            results.append("✅ Visible Test Case 2 Passed: Convert to Fahrenheit")
        else:
            results.append("❌ Visible Test Case 2 Failed: Convert to Fahrenheit")
    except Exception as e:
        results.append(f"❌ Visible Test Case 2 Failed: Convert to Fahrenheit ({e})")

    try:
        result = solution.calculate_average_temperature(np.array([10, 20, 30]))
        if isinstance(result, float):
            results.append("✅ Visible Test Case 3 Passed: Calculate average temperature")
        else:
            results.append("❌ Visible Test Case 3 Failed: Calculate average temperature")
    except Exception as e:
        results.append(f"❌ Visible Test Case 3 Failed: Calculate average temperature ({e})")

    try:
        result = solution.categorize_temperature(np.array([5, 15, 30]))
        if isinstance(result, np.ndarray):
            results.append("✅ Visible Test Case 4 Passed: Categorize temperature")
        else:
            results.append("❌ Visible Test Case 4 Failed: Categorize temperature")
    except Exception as e:
        results.append(f"❌ Visible Test Case 4 Failed: Categorize temperature ({e})")

    # HIDDEN TEST CASES
    try:
        result = solution.convert_to_fahrenheit(np.array([37]))
        if np.allclose(result, [98.6]):
            results.append("✅ Hidden Test Case 1 Passed: Edge conversion (37°C)")
        else:
            results.append("❌ Hidden Test Case 1 Failed: Edge conversion (37°C)")
    except Exception as e:
        results.append(f"❌ Hidden Test Case 1 Failed: Edge conversion (37°C) ({e})")

    try:
        result = solution.categorize_temperature(np.array([10, 25]))
        if isinstance(result, np.ndarray):
            results.append("✅ Hidden Test Case 2 Passed: Categorization boundaries")
        else:
            results.append("❌ Hidden Test Case 2 Failed: Categorization boundaries")
    except Exception as e:
        results.append(f"❌ Hidden Test Case 2 Failed: Categorization boundaries ({e})")

    # OUTPUT to console and report
    for line in results:
        print(line)

    report_folder = os.path.join(os.path.dirname(solution_path), "reports")
    os.makedirs(report_folder, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(os.path.join(report_folder, f"report_{timestamp}.txt"), "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")
