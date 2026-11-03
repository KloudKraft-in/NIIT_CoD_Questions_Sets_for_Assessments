import pandas as pd
import os
import sys
import importlib.util

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}")
        return
    
    print("Running Tests for: Patient Health Monitor (Strict Method Independence)\n")
    report_lines = ["Running Tests for: Patient Health Monitor (Strict Method Independence)\n"]
    
    if not hasattr(solution, "HealthMonitor"):
        print("ERROR: HealthMonitor class not found")
        return
    
    HealthMonitor = solution.HealthMonitor
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    health_csv = os.path.join(data_dir, 'health.csv')
    
    # Isolated Reference Data
    raw_df = pd.read_csv(health_csv)
    cleaned_df = raw_df.dropna().copy()
    
    test_cases = [
        {"desc": "Initial State (Sample)", "type": "sample", "expected": None},
        {"desc": "Data Loading (Sample)", "type": "sample", "expected": 12},
        {"desc": "Clean Records (Logic)", "type": "marked", "func": "clean_records", "expected": 2},
        {"desc": "Find Highest Rate (Logic)", "type": "marked", "func": "find_highest_rate", "expected": 110},
        {"desc": "Patient Averages (Logic)", "type": "marked", "func": "patient_averages", "expected": 72.33},
        {"desc": "High Risk Identification (Logic)", "type": "marked", "func": "high_risk", "expected": ['P03']},
        {"desc": "Count High Risk Patients (Logic)", "type": "marked", "func": "count_high_risk", "expected": 1}
    ]

    total_score = 0
    max_score = 20.0

    for idx, case in enumerate(test_cases, 1):
        try:
            temp = HealthMonitor()
            actual = None
            
            if idx == 1: # init state
                actual = temp.df
            elif idx == 2: # data loading
                temp.read_data(health_csv)
                actual = len(temp.df) if temp.df is not None else 0
            elif idx == 3: # clean_records
                temp.df = raw_df.copy()
                actual = temp.clean_records()
            elif idx == 4: # find_highest_rate
                temp.df = cleaned_df.copy()
                actual = temp.find_highest_rate()
            elif idx == 5: # patient_averages
                temp.df = cleaned_df.copy()
                res = temp.patient_averages()
                actual = round(res.get('P01', 0), 2) if isinstance(res, dict) else res
            elif idx == 6: # high_risk
                temp.df = cleaned_df.copy()
                actual = temp.high_risk(100)
            elif idx == 7: # count_high_risk
                temp.df = cleaned_df.copy()
                # ENSURE INDEPENDENCE: Mock high_risk so TC7 doesn't fail if Method 6 is buggy
                temp.high_risk = lambda threshold: ['P03'] if threshold == 100 else []
                actual = temp.count_high_risk(100)
            
            if actual == case["expected"]:
                if case["type"] == "marked":
                    msg = f"PASS TC{idx} [{case['desc']}] (4/4)"
                    total_score += 4
                else:
                    msg = f"PASS TC{idx} [{case['desc']}] (Sample)"
            else:
                msg = f"FAIL TC{idx} [{case['desc']}] | Expected: {case['expected']}, Got: {actual}"
            
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}] | Error: {str(e)}"
        
        print(msg)
        report_lines.append(msg)

    print(f"\nSCORE: {total_score}/{max_score}")
    report_lines.append(f"\nSCORE: {total_score}/{max_score}")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
