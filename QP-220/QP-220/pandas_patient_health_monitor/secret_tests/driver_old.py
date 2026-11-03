import pandas as pd
import numpy as np
import os
import sys
import importlib.util
import random

def resolve_csv_path():
    paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "health_old.csv"),
        os.path.join(os.path.dirname(__file__), "health_old.csv")
    ]
    for p in paths:
        if os.path.exists(p): return p
    return None

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    import traceback
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}")
        traceback.print_exc()
        return
    
    print("Running Tests for: Patient Health Monitor\n")
    report_lines = ["Running Tests for: Patient Health Monitor\n"]
    
    if not hasattr(solution, "HealthMonitor"):
        print("ERROR: HealthMonitor class not found"); return
    
    HealthMonitor = solution.HealthMonitor
    csv_file = resolve_csv_path()
    
    try:
        if csv_file and os.path.exists(csv_file):
            raw_df = pd.read_csv(csv_file)
        else:
            raw_df = pd.DataFrame({
                'PatientID': ['P01', 'P02', 'P01', 'P03', 'P04', 'P05', 'P06', 'P01', 'P03', 'P04', 'P02', 'P05'],
                'Day': ['Mon', 'Mon', 'Tue', 'Mon', 'Tue', 'Mon', 'Mon', 'Wed', 'Tue', 'Wed', 'Tue', 'Wed'],
                'HeartRate': [72.0, np.nan, 75.0, 105.0, 68.0, 80.0, np.nan, 70.0, 110.0, 75.0, 85.0, 90.0]
            })
        cleaned_df = raw_df.dropna(subset=['HeartRate']).copy()
    except Exception as e:
        print(f"ERROR: Failed to load raw data: {e}")
        traceback.print_exc()
        return

    tc_configs = [
        ("Initial State", 0),
        ("Data Loading", 0),
        ("Clean Records", 4),
        ("Find Highest Rate", 4),
        ("Patient Averages", 4),
        ("High Risk Identification", 4),
        ("Count High Risk Patients", 4)
    ]

    total_score = 0
    for i, (desc, marks) in enumerate(tc_configs, 1):
        try:
            def run_t(idx, current_obj, current_df=None):
                if idx == 1: return current_obj.df
                if idx == 2: current_obj.read_data(csv_file); return len(current_obj.df) if current_obj.df is not None else 0
                if idx == 3: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.clean_records()
                if idx == 4: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.find_highest_rate()
                if idx == 5: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.patient_averages()
                if idx == 6: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.high_risk(100)
                if idx == 7: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.count_high_risk(100)
                return None

            p_ok, h_det, none_ret = False, False, False
            
            if i <= 2: # Samples
                res2 = run_t(i, HealthMonitor())
                exp2 = None if i == 1 else 12
                p_ok = (res2 is None or res2 == exp2 or (i==2 and res2 > 0))
            else:
                rv = random.randint(110, 150)
                
                # Setup base runs
                obj1 = HealthMonitor()
                if i == 3:
                    res1 = run_t(i, obj1, raw_df)
                else:
                    res1 = run_t(i, obj1, cleaned_df)
                
                # Setup dynamic runs
                obj2 = HealthMonitor()
                if i == 3:
                    # In dyn_df, make one more record NaN
                    dyn_df = raw_df.copy()
                    for idx in range(len(dyn_df)):
                        if not pd.isna(dyn_df.loc[idx, 'HeartRate']):
                            dyn_df.loc[idx, 'HeartRate'] = np.nan
                            break
                    res2 = run_t(i, obj2, dyn_df)
                    exp2 = 3
                else:
                    dyn_df = cleaned_df.copy()
                    for idx in range(len(dyn_df)):
                        if dyn_df.loc[idx, 'PatientID'] == 'P01':
                            dyn_df.loc[idx, 'HeartRate'] = float(rv)
                            break
                    res2 = run_t(i, obj2, dyn_df)
                    
                    if i == 4:
                        exp2 = float(rv)
                    elif i == 5:
                        p01_vals = dyn_df[dyn_df['PatientID'] == 'P01']['HeartRate'].tolist()
                        exp2 = {
                            'P01': round(sum(p01_vals) / len(p01_vals), 2),
                            'P03': 107.50,
                            'P04': 71.50,
                            'P05': 85.00,
                            'P02': 85.00
                        }
                    elif i == 6:
                        exp2 = ['P01', 'P03'] if rv > 100 else ['P03']
                    elif i == 7:
                        exp2 = 2 if rv > 100 else 1

                if res2 == exp2: p_ok = True
                elif res2 is None: none_ret = True
                elif res1 == res2: h_det = True

            if p_ok:
                total_score += marks
                msg = f"PASS TC{i} [{desc}] ({marks if marks > 0 else 'Sample'})"
            elif none_ret:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Method not implemented / No return value"
            elif h_det:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Hardcoded. Dynamic check failed."
            else:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Incorrect Output. Expected: {exp2} | Actual: {res2}"
        except Exception as e:
            msg = f"FAIL TC{i} [{desc}] | Error: {e}\n{traceback.format_exc()}"
        print(msg); report_lines.append(msg)

    print(f"\nSCORE: {total_score}/20.0")
    report_lines.append(f"\nSCORE: {total_score}/20.0")
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
