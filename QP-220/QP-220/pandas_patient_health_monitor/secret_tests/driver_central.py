from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
import os
import sys
import importlib.util
import random
import re
import traceback

# Global IST offset for consistent reporting
ist_offset = timezone(timedelta(hours=5, minutes=30))

def get_timestamp():
    """Returns timestamp in YYYYMMDD_HHMMSS format (IST assumption)"""
    return datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")

# UPDATE 1: Added exam_code="UNKNOWN"
def test_student_code(solution_path, vm_tag="DEFAULT", exam_code="UNKNOWN"):
    problem_code = "pandas_patient_health_monitor"
    
    if vm_tag is None:
        vm_tag = "DEFAULT"
        
    # Extract username and timestamp from vm_tag if it's in the server structure
    match = re.search(r'TRIAL_([^_]+)_(\d{8}_\d{6})', vm_tag)
    if match:
        username, timestamp = match.groups()
    else:
        username = vm_tag
        timestamp = get_timestamp()

    # Reporting setup for central server with robust write-access check
    report_base = f"/home/ubuntu/central_server/reports/{problem_code}/{username}"
    has_server_access = False
    try:
        os.makedirs(report_base, exist_ok=True)
        report_path = os.path.join(report_base, f"{username}_{timestamp}.txt")
        # Test write permission
        test_file = os.path.join(report_base, f".write_test_{timestamp}")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        has_server_access = True
    except Exception:
        has_server_access = False

    # Fallback for local testing or if server path is not writable
    if not has_server_access or not os.path.exists("/home/ubuntu/central_server"):
        report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, f"{username}_{timestamp}.txt")

    results = [f">> Testing solution for {username} at {timestamp}"]
    
    # UPDATE 2: Added this line to print the exam code into the .txt report
    results.append(f"EXAM CODE: {exam_code}")
    
    report_items = []
    total_score = 0
    fail_count = 0

    # Wrap the entire test logic in a global try-except to guarantee report generation
    try:
        # Safe CSV path resolution checking both names
        csv_file = None
        possible_csv_paths = [
            "/home/ubuntu/central_server/data/health_old.csv",
            "/home/ubuntu/central_server/data/health.csv",
            os.path.join(os.path.dirname(__file__), "..", "data", "health_old.csv"),
            os.path.join(os.path.dirname(__file__), "..", "data", "health.csv"),
            os.path.join(os.path.dirname(__file__), "health_old.csv"),
            os.path.join(os.path.dirname(__file__), "health.csv")
        ]
        for p in possible_csv_paths:
            if os.path.exists(p):
                csv_file = p
                break
        
        if not csv_file:
            csv_file = "health_old.csv" # Fallback filename string for read_data call

        try:
            spec = importlib.util.spec_from_file_location("solution", solution_path)
            solution = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(solution)
            HealthMonitor = solution.HealthMonitor
        except Exception as e:
            err_detail = f"IMPORT ERROR: Failed to load HealthMonitor: {e}\n{traceback.format_exc()}"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(err_detail + "\n")
            print(err_detail)
            return

        # Load CSV or fallback to in-memory DataFrame
        try:
            if csv_file and os.path.exists(csv_file):
                raw_df = pd.read_csv(csv_file)
            else:
                # In-memory backup matching health_old.csv exactly
                raw_df = pd.DataFrame({
                    'PatientID': ['P01', 'P02', 'P01', 'P03', 'P04', 'P05', 'P06', 'P01', 'P03', 'P04', 'P02', 'P05'],
                    'Day': ['Mon', 'Mon', 'Tue', 'Mon', 'Tue', 'Mon', 'Mon', 'Wed', 'Tue', 'Wed', 'Tue', 'Wed'],
                    'HeartRate': [72.0, np.nan, 75.0, 105.0, 68.0, 80.0, np.nan, 70.0, 110.0, 75.0, 85.0, 90.0]
                })
            cleaned_df = raw_df.dropna(subset=['HeartRate']).copy()
        except Exception as e:
            # Safe absolute fallback
            raw_df = pd.DataFrame({
                'PatientID': ['P01', 'P02', 'P01', 'P03', 'P04', 'P05', 'P06', 'P01', 'P03', 'P04', 'P02', 'P05'],
                'Day': ['Mon', 'Mon', 'Tue', 'Mon', 'Tue', 'Mon', 'Mon', 'Wed', 'Tue', 'Wed', 'Tue', 'Wed'],
                'HeartRate': [72.0, np.nan, 75.0, 105.0, 68.0, 80.0, np.nan, 70.0, 110.0, 75.0, 85.0, 90.0]
            })
            cleaned_df = raw_df.dropna(subset=['HeartRate']).copy()

        tc_configs = [
            ("Initial State", 0),
            ("Data Loading", 0),
            ("Clean Records", 4),
            ("Find Highest Rate", 4),
            ("Patient Averages", 4),
            ("High Risk Identification", 4),
            ("Count High Risk Patients", 4)
        ]
        
        total_tc = len(tc_configs)
        print(f"Running Evaluation for: {problem_code}\n")
        print(f"{'Test Case':<15} | {'Status':<10} | {'Marks'}")
        print("-" * 50)
        
        random.seed(None)
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
                if i <= 2:
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
     
                tc_name = f"TC{i} [{desc}]"
                report_items.append(tc_name)
                
                if p_ok:
                    total_score += marks
                    status = "PASSED"
                    results.append(f"✓ {tc_name}: PASSED ({marks if marks > 0 else 'Sample'})")
                else:
                    status = "FAILED"
                    fail_count += 1
                    if none_ret:
                        reason = "Method not implemented / No return value"
                    elif h_det:
                        reason = "Hardcoded. Dynamic check failed."
                    else:
                        reason = f"Incorrect Output. Expected: {exp2} | Actual: {res2}"
                    results.append(f"✗ {tc_name}: FAILED (0/{marks}) | {reason}")
                    
                print(f"TC{i:02d} [{desc[:30]:<30}] | {status:<10} | {marks if status == 'PASSED' else 0}/{marks}")
     
            except Exception as e:
                status = "FAILED"
                fail_count += 1
                results.append(f"✗ TC{i} [{desc}]: FAILED (0/{marks}) | Error: {e}\n{traceback.format_exc()}")
                print(f"TC{i:02d} [{desc[:30]:<30}] | {status:<10} | 0/{marks}")

        print("-" * 50)
        print(f"{'TOTAL SCORE':<15} | {'':<10} | {total_score}/20")
        results.append(f"\n🎯 TOTAL SCORE: {total_score}/20")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(results) + "\n")

        # Final Standardized CSV Output (8-Column Format)
        date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
        csv_report = f"{date_str},{problem_code},{username},{timestamp},{total_tc}: {'; '.join(report_items)},,{fail_count},{total_score}"
        print(f"\n[REPORT_CSV]: {csv_report}")

    except Exception as e:
        critical_err = f"CRITICAL EVALUATION FAILURE: {e}\n{traceback.format_exc()}"
        print(critical_err)
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(critical_err + "\n")
        except Exception:
            pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2] if len(sys.argv) > 2 else None
        
        # UPDATE 3: Allow passing the 3rd argument (exam_code) when calling directly
        arg3 = sys.argv[3] if len(sys.argv) > 3 else "UNKNOWN"
        
        if arg1.endswith(".py") or "/" in arg1 or "\\" in arg1 or os.path.exists(arg1):
            sol = os.path.abspath(arg1)
            vm = arg2 if arg2 else "DEFAULT"
        else:
            vm = arg1
            sol = os.path.abspath(arg2) if arg2 else os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    else:
        vm = "DEFAULT"
        sol = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
        arg3 = "UNKNOWN"
        
    test_student_code(sol, vm, arg3)
