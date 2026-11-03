import importlib.util
import traceback
import numpy as np
import os

def test_student_code(solution_path):
    report_lines = []
    total_score = 0
    max_score = 10

    spec = importlib.util.spec_from_file_location("solution", solution_path)
    student_code = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_code)

    try:
        obj = student_code.ShoppingBillCalculator()
    except Exception as e:
        report_lines.append("❌ Could not instantiate  class.")
        report_lines.append(str(e))
        write_report(report_lines, total_score, max_score)
        return

    # ✅ Test Case 1: create_price_array
    try:
        result = obj.create_price_array([100, 200, 300])
        expected = np.array([100., 200., 300.])
        if np.array_equal(result, expected):
            report_lines.append("✅ Visible Test Case 1 Passed: create_price_array()")
            total_score += 2
        else:
            report_lines.append("❌ Visible Test Case 1 Failed: create_price_array()")
    except Exception:
        report_lines.append("❌ Visible Test Case 1 Error: create_price_array()")
        report_lines.append(traceback.format_exc())

    # ✅ Test Case 2: calculate_total_cost
    try:
        result = obj.calculate_total_cost(np.array([100., 200.]), np.array([2, 1]))
        if result == 400.0:
            report_lines.append("✅ Visible Test Case 2 Passed: calculate_total_cost()")
            total_score += 2
        else:
            report_lines.append("❌ Visible Test Case 2 Failed: calculate_total_cost()")
    except Exception:
        report_lines.append("❌ Visible Test Case 2 Error: calculate_total_cost()")
        report_lines.append(traceback.format_exc())

    # ✅ Test Case 3: apply_discount
    try:
        result = obj.apply_discount(np.array([100., 200.]), 10)
        expected = np.array([90., 180.])
        if np.allclose(result, expected):
            report_lines.append("✅ Visible Test Case 3 Passed: apply_discount()")
            total_score += 2
        else:
            report_lines.append("❌ Visible Test Case 3 Failed: apply_discount()")
    except Exception:
        report_lines.append("❌ Visible Test Case 3 Error: apply_discount()")
        report_lines.append(traceback.format_exc())

    # 🤐 Hidden Test Case 1: 100% Discount
    try:
        result = obj.apply_discount(np.array([99.]), 100)
        expected = np.array([0.])
        if np.allclose(result, expected):
            report_lines.append("✅ Hidden Test Case 1 Passed: 100% Discount Edge")
            total_score += 2
        else:
            report_lines.append("❌ Hidden Test Case 1 Failed: 100% Discount Edge")
    except Exception:
        report_lines.append("❌ Hidden Test Case 1 Error: apply_discount()")
        report_lines.append(traceback.format_exc())

    # 🤐 Hidden Test Case 2: filter_items_above_threshold
    try:
        result = obj.filter_items_above_threshold(np.array([30., 50., 100.]), 50)
        expected = np.array([100.])
        if np.array_equal(result, expected):
            report_lines.append("✅ Hidden Test Case 2 Passed: filter_items_above_threshold()")
            total_score += 2
        else:
            report_lines.append("❌ Hidden Test Case 2 Failed: filter_items_above_threshold()")
    except Exception:
        report_lines.append("❌ Hidden Test Case 2 Error: filter_items_above_threshold()")
        report_lines.append(traceback.format_exc())

    write_report(report_lines, total_score, max_score)

def write_report(lines, score, max_score):
    lines.append("\n🎯 TOTAL SCORE: {}/{}".format(score, max_score))
    
    # Create reports directory
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))
    os.makedirs(reports_dir, exist_ok=True)
    
    # Determine next report filename
    existing = [f for f in os.listdir(reports_dir) if f.startswith("report") and f.endswith(".txt")]
    report_filename = f"report_{len(existing)+1}.txt"
    report_path = os.path.join(reports_dir, report_filename)
    
    # Write to file and also print
    with open(report_path, "w", encoding="utf-8") as f:
        for line in lines:
            print(line)
            f.write(line + "\n")
    
    print(f"\n📁 Report saved as: {report_filename}")
