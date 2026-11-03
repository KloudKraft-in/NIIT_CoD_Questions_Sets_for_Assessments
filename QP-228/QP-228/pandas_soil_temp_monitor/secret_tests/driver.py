import pandas as pd
import numpy as np
import os
import sys
import importlib.util
import random

def resolve_csv_path():
    paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "temperature.csv"),
        os.path.join(os.path.dirname(__file__), "temperature.csv")
    ]
    for p in paths:
        if os.path.exists(p): return p
    return None

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return
    
    print("Running Tests for: Soil Temperature Monitor\n")
    report_lines = ["Running Tests for: Soil Temperature Monitor\n"]
    
    if not hasattr(solution, "SoilTempMonitor"):
        print("ERROR: SoilTempMonitor class not found"); return
    
    SoilTempMonitor = solution.SoilTempMonitor
    csv_file = resolve_csv_path()
    
    try:
        raw_df = pd.read_csv(csv_file)
        cleaned_df = raw_df.dropna(subset=['Temperature']).copy()
    except Exception as e:
        print(f"ERROR: Failed to load raw data: {e}")
        return

    tc_configs = [
        ("Initial State", 0),
        ("Data Loading", 0),
        ("Clean Records", 4),
        ("Find Highest Temp", 4),
        ("Sensor Averages", 4),
        ("High Temp Sensors", 4),
        ("Count High Temp Sensors", 4)
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
                    return current_obj.find_highest_temp()
                if idx == 5: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.sensor_averages()
                if idx == 6: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.high_temp_sensors(40)
                if idx == 7: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.count_high_temp_sensors(40)
                return None

            p_ok, h_det, none_ret = False, False, False
            
            if i <= 2: # Samples
                res2 = run_t(i, SoilTempMonitor())
                exp2 = None if i == 1 else 12
                p_ok = (res2 is None or res2 == exp2 or (i==2 and res2 > 0))
            else:
                rv = random.randint(50, 75)
                
                # Setup base runs
                obj1 = SoilTempMonitor()
                if i == 3:
                    res1 = run_t(i, obj1, raw_df)
                else:
                    res1 = run_t(i, obj1, cleaned_df)
                
                # Setup dynamic runs
                obj2 = SoilTempMonitor()
                if i == 3:
                    # In dyn_df, make one more record NaN
                    dyn_df = raw_df.copy()
                    for idx in range(len(dyn_df)):
                        if not pd.isna(dyn_df.loc[idx, 'Temperature']):
                            dyn_df.loc[idx, 'Temperature'] = np.nan
                            break
                    res2 = run_t(i, obj2, dyn_df)
                    exp2 = 3
                else:
                    dyn_df = cleaned_df.copy()
                    for idx in range(len(dyn_df)):
                        if dyn_df.loc[idx, 'SensorID'] == 'S01':
                            dyn_df.loc[idx, 'Temperature'] = float(rv)
                            break
                    res2 = run_t(i, obj2, dyn_df)
                    
                    if i == 4:
                        exp2 = float(rv)
                    elif i == 5:
                        s01_vals = dyn_df[dyn_df['SensorID'] == 'S01']['Temperature'].tolist()
                        exp2 = {
                            'S01': round(sum(s01_vals) / len(s01_vals), 2),
                            'S03': 43.50,
                            'S04': 31.50,
                            'S05': 39.00,
                            'S02': 36.00
                        }
                    elif i == 6:
                        exp2 = ['S01', 'S03'] if rv > 40 else ['S03']
                    elif i == 7:
                        exp2 = 2 if rv > 40 else 1

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
        except Exception as e: msg = f"FAIL TC{i} [{desc}] | Error: {e}"
        print(msg); report_lines.append(msg)

    print(f"\nSCORE: {total_score}/20.0")
    report_lines.append(f"\nSCORE: {total_score}/20.0")
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")
