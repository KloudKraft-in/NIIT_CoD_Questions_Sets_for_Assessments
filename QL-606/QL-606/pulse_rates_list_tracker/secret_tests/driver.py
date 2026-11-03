import importlib.util
import os
import sys
import random
import copy

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable."
    return True, None

# Embedded Reference Logic for Grading (Oracle)
class _GradingLogic:
    @staticmethod
    def patient_averages(records):
        if not records:
            return {}
        groups = {}
        for r in records:
            if r[2] is not None:
                pid = r[0]
                groups.setdefault(pid, []).append(r[2])
        
        averages = {}
        for pid, rates in groups.items():
            averages[pid] = round(sum(rates) / len(rates), 2)
        return averages

    @staticmethod
    def high_risk(records, threshold):
        if not records:
            return []
        high_risk_pts = set()
        for r in records:
            if r[2] is not None and r[2] > threshold:
                high_risk_pts.add(r[0])
        return sorted(list(high_risk_pts))

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    # Load Student Solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        msg = f"IMPORT ERROR: {e}"
        print(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write(msg + "\n")
        return

    print("Running Tests for: Pulse Rates List Tracker\n")
    report_lines = ["Running Tests for: Pulse Rates List Tracker\n"]

    if not hasattr(solution, "HealthMonitor"):
        msg = "ERROR: HealthMonitor class not found in solution.py"
        print(msg); report_lines.append(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")
        return

    # Default base records for reference
    default_records = [
        ['P01', 'Mon', 72],
        ['P02', 'Mon', None],
        ['P01', 'Tue', 75],
        ['P03', 'Mon', 105],
        ['P04', 'Tue', 68],
        ['P05', 'Mon', 80],
        ['P06', 'Mon', None],
        ['P01', 'Wed', 70],
        ['P03', 'Tue', 110],
        ['P04', 'Wed', 75],
        ['P02', 'Tue', 85],
        ['P05', 'Wed', 90]
    ]

    test_cases = [
        {
            "desc": "Verification of list initialization",
            "func": "__init__",
            "setup": lambda: solution.HealthMonitor(),
            "call": lambda obj: obj.records,
            "check": lambda res: res == default_records,
            "expected_output": "Should initialize self.records with default records list.",
            "marks": 0
        },
        {
            "desc": "Strategic cleaning of null records",
            "func": "clean_records",
            "setup": lambda: solution.HealthMonitor(),
            "call": lambda obj: (obj.clean_records(), len(obj.records)),
            "check": lambda res: res == (2, 10),
            "expected_output": "Should drop 2 records containing None values in HeartRate.",
            "marks": 4
        },
        {
            "desc": "Identify the highest recorded heart rate",
            "func": "find_highest_rate",
            "setup": lambda: solution.HealthMonitor(),
            "call": lambda obj: (obj.clean_records(), obj.find_highest_rate())[1],
            "check": lambda res: res == 110,
            "expected_output": "Expected peak heart rate 110.",
            "marks": 4
        },
        {
            "desc": "Calculate averages per patient ID",
            "func": "patient_averages",
            "setup": lambda: solution.HealthMonitor(),
            "call": lambda obj: (obj.clean_records(), obj.patient_averages())[1],
            "check": lambda res: res == _GradingLogic.patient_averages([r for r in default_records if r[2] is not None]),
            "expected_output": "Should calculate average heart rate per patient.",
            "marks": 4
        },
        {
            "desc": "Identify patients exceeding threshold",
            "func": "high_risk",
            "setup": lambda: solution.HealthMonitor(),
            "call": lambda obj: (obj.clean_records(), obj.high_risk(100))[1],
            "check": lambda res: res == _GradingLogic.high_risk([r for r in default_records if r[2] is not None], 100),
            "expected_output": "Should find ['P03'] exceeding 100.",
            "marks": 4
        },
        {
            "desc": "Count unique high-risk patients",
            "func": "count_high_risk",
            "setup": lambda: solution.HealthMonitor(),
            "call": lambda obj: (obj.clean_records(), obj.count_high_risk(100))[1],
            "check": lambda res: res == len(_GradingLogic.high_risk([r for r in default_records if r[2] is not None], 100)),
            "expected_output": "Expected 1 unique patient exceeding 100.",
            "marks": 4
        }
    ]

    total_score = 0
    for idx, case in enumerate(test_cases, 1):
        marks = case["marks"]
        try:
            obj = case["setup"]()
            valid, err = validate_method_exists(obj, case["func"])
            if not valid:
                msg = f"FAIL TC{idx} [{case['desc']}]: {err}"
                print(msg); report_lines.append(msg); continue

            result = case["call"](obj)
            passed = case["check"](result)

            if passed:
                total_score += marks
                msg = f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})"
            else:
                msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks})\n  Expected: {case['expected_output']}\n  Got: {repr(result)}"
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks}) | Error: {type(e).__name__}: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/20.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
