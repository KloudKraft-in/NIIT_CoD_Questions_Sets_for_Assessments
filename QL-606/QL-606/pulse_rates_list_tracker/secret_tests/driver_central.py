import importlib.util
import os
import sys
import random
import re
import traceback
import copy
from datetime import datetime, timezone, timedelta

def get_ist_time():
    try:
        ist = timezone(timedelta(hours=5, minutes=30))
        return datetime.now(ist).strftime("%Y%m%d_%H%M%S")
    except:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

def validate_method_exists(obj, method_name):
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' is not callable."
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

def test_student_code(solution_path, vm_tag="DEFAULT"):
    # 1. Robust Path and Slug Discovery
    try:
        current_file_path = os.path.abspath(__file__)
        slug = os.path.basename(os.path.dirname(current_file_path))
    except:
        slug = "pulse_rates_list_tracker"

    # 2. Report Path Resolution
    match = re.search(r'(.+)_(\d{8}_\d{6})', vm_tag)
    if match:
        username, timestamp = match.groups()
    else:
        username, timestamp = vm_tag, get_ist_time()

    report_base = f"/home/ubuntu/central_server/reports/{slug}/{username}"
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{username}_{timestamp}.txt")

    results = [f"Running Tests for: {slug} (Central Server)\n"]
    total_score = 0

    try:
        # 3. Load Student Solution with Absolute Path
        abs_solution_path = os.path.abspath(solution_path)
        if not os.path.exists(abs_solution_path):
            raise FileNotFoundError(f"Solution file not found at {abs_solution_path}")

        spec = importlib.util.spec_from_file_location("solution", abs_solution_path)
        solution = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(solution)
        
        if not hasattr(solution, "HealthMonitor"):
            results.append("ERROR: HealthMonitor class not found in solution.py")
        else:
            tc_configs = [
                {"desc": "Verification of list initialization", "func": "__init__", "m": 0},
                {"desc": "Strategic cleaning of null records", "func": "clean_records", "m": 4},
                {"desc": "Identify the highest recorded heart rate", "func": "find_highest_rate", "m": 4},
                {"desc": "Calculate averages per patient ID", "func": "patient_averages", "m": 4},
                {"desc": "Identify patients exceeding threshold", "func": "high_risk", "m": 4},
                {"desc": "Count unique high-risk patients", "func": "count_high_risk", "m": 4}
            ]
            
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

            for idx, case in enumerate(tc_configs, 1):
                marks = float(case["m"])
                try:
                    monitor = solution.HealthMonitor()
                    valid, err = validate_method_exists(monitor, case["func"])
                    if not valid:
                         results.append(f"FAIL TC{idx} [{case['desc']}]: {err}")
                         continue

                    # Random offset for dynamic testing
                    rv = random.randint(115, 150)

                    p_ok = False
                    if idx == 1: 
                        p_ok = (monitor.records == default_records)
                    elif idx == 2:
                        monitor.records = copy.deepcopy(default_records)
                        monitor.records[0][2] = None
                        p_ok = (monitor.clean_records() == 3 and len(monitor.records) == 9)
                    elif idx == 3:
                        cleaned_recs = [r for r in default_records if r[2] is not None]
                        cleaned_recs[0][2] = rv
                        monitor.records = copy.deepcopy(cleaned_recs)
                        p_ok = (monitor.find_highest_rate() == rv)
                    elif idx == 4:
                        cleaned_recs = [r for r in default_records if r[2] is not None]
                        cleaned_recs[0][2] = rv
                        monitor.records = copy.deepcopy(cleaned_recs)
                        p_ok = (monitor.patient_averages() == _GradingLogic.patient_averages(cleaned_recs))
                    elif idx == 5:
                        cleaned_recs = [r for r in default_records if r[2] is not None]
                        cleaned_recs[0][2] = rv
                        monitor.records = copy.deepcopy(cleaned_recs)
                        p_ok = (monitor.high_risk(100) == _GradingLogic.high_risk(cleaned_recs, 100))
                    elif idx == 6:
                        cleaned_recs = [r for r in default_records if r[2] is not None]
                        cleaned_recs[0][2] = rv
                        monitor.records = copy.deepcopy(cleaned_recs)
                        p_ok = (monitor.count_high_risk(100) == len(_GradingLogic.high_risk(cleaned_recs, 100)))

                    if p_ok: 
                        total_score += marks
                        results.append(f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})")
                    else: 
                        results.append(f"FAIL TC{idx} [{case['desc']}] (0/{marks}) - Incorrect Output.")
                except Exception as e:
                    results.append(f"FAIL TC{idx} [{case['desc']}] | Error: {type(e).__name__}")

    except Exception as e:
        results.append(f"CRITICAL SYSTEM ERROR: {traceback.format_exc()}")

    results.append(f"\nSCORE: {total_score}/20 (Visible) | {total_score}/20 (Total)")
    print("\n".join(results))
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results) + "\n")

if __name__ == "__main__":
    v_tag = sys.argv[1] if len(sys.argv) > 1 else "DEFAULT"
    s_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(s_path, v_tag)
