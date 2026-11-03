from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
import os
import sys
import importlib.util
import random
import re

# Global IST offset for consistent reporting
ist_offset = timezone(timedelta(hours=5, minutes=30))

def get_timestamp():
    """Returns timestamp in YYYYMMDD_HHMMSS format (IST assumption)"""
    return datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")

def test_student_code(solution_path, vm_tag="DEFAULT"):
    problem_code = "pandas_server_latency_monitor"
    
    if vm_tag is None:
        vm_tag = "DEFAULT"
        
    # Extract username and timestamp from vm_tag if it's in the server structure
    match = re.search(r'TRIAL_([^_]+)_(\d{8}_\d{6})', vm_tag)
    if match:
        username, timestamp = match.groups()
    else:
        username = vm_tag
        timestamp = get_timestamp()

    # Reporting setup for central server
    report_base = f"/home/ubuntu/central_server/reports/{problem_code}/{username}"
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{username}_{timestamp}.txt")
    
    # Fallback for local testing
    if not os.path.exists("/home/ubuntu/central_server"):
        report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, f"{username}_{timestamp}.txt")

    csv_file = "/home/ubuntu/central_server/data/latency.csv"
    if not os.path.exists(csv_file):
        csv_file = os.path.join(os.path.dirname(__file__), "..", "data", "latency.csv")

    results = [f">> Testing solution for {username} at {timestamp}"]
    report_items = []
    total_score = 0
    fail_count = 0
    
    try:
        spec = importlib.util.spec_from_file_location("solution", solution_path)
        solution = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(solution)
        ServerLatencyMonitor = solution.ServerLatencyMonitor
    except Exception as e:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"IMPORT ERROR: {e}\n")
        print(f"IMPORT ERROR: {e}")
        return

    
    try:
        raw_df = pd.read_csv(csv_file)
        cleaned_df = raw_df.dropna(subset=['Latency']).copy()
    except Exception as e:
        print(f"ERROR: Failed to load raw data: {e}")
        return

    tc_configs = [
        ("Initial State", 0),
        ("Data Loading", 0),
        ("Clean Records", 4),
        ("Find Highest Latency", 4),
        ("Endpoint Averages", 4),
        ("High Latency Endpoints", 4),
        ("Count High Latency Endpoints", 4)
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
                    return current_obj.find_highest_latency()
                if idx == 5: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.endpoint_averages()
                if idx == 6: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.high_latency_endpoints(200)
                if idx == 7: 
                    if current_df is not None: current_obj.df = current_df.copy()
                    return current_obj.count_high_latency_endpoints(200)
                return None

            p_ok, h_det, none_ret = False, False, False
            if i <= 2:
                res2 = run_t(i, ServerLatencyMonitor())
                exp2 = None if i == 1 else 12
                p_ok = (res2 is None or res2 == exp2 or (i==2 and res2 > 0))
            else:
                rv = random.randint(220, 350)
                
                # Setup base runs
                obj1 = ServerLatencyMonitor()
                if i == 3:
                    res1 = run_t(i, obj1, raw_df)
                else:
                    res1 = run_t(i, obj1, cleaned_df)
                
                # Setup dynamic runs
                obj2 = ServerLatencyMonitor()
                if i == 3:
                    # In dyn_df, make one more record NaN
                    dyn_df = raw_df.copy()
                    for idx in range(len(dyn_df)):
                        if not pd.isna(dyn_df.loc[idx, 'Latency']):
                            dyn_df.loc[idx, 'Latency'] = np.nan
                            break
                    res2 = run_t(i, obj2, dyn_df)
                    exp2 = 3
                else:
                    dyn_df = cleaned_df.copy()
                    for idx in range(len(dyn_df)):
                        if dyn_df.loc[idx, 'EndpointID'] == 'E01':
                            dyn_df.loc[idx, 'Latency'] = float(rv)
                            break
                    res2 = run_t(i, obj2, dyn_df)
                    
                    if i == 4:
                        exp2 = float(rv) if rv > 500 else 500.0
                    elif i == 5:
                        e01_vals = dyn_df[dyn_df['EndpointID'] == 'E01']['Latency'].tolist()
                        exp2 = {
                            'E01': round(sum(e01_vals) / len(e01_vals), 2),
                            'E03': 425.00,
                            'E04': 124.00,
                            'E05': 185.00,
                            'E02': 160.00
                        }
                    elif i == 6:
                        exp2 = ['E01', 'E03'] if rv > 200 else ['E03']
                    elif i == 7:
                        exp2 = 2 if rv > 200 else 1
                
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
            results.append(f"✗ TC{i} [{desc}]: FAILED (0/{marks}) | Error: {e}")
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

if __name__ == "__main__":
    vm = sys.argv[1] if len(sys.argv) > 1 else "DEFAULT"
    sol = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol, vm)
