from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
import os
import sys
import importlib.util
import random
import re
import inspect
import traceback
import warnings

# Suppress all pandas/setting-with-copy warnings
warnings.filterwarnings("ignore")

# Global IST offset for consistent reporting
ist_offset = timezone(timedelta(hours=5, minutes=30))

def get_timestamp():
    """Returns timestamp in YYYYMMDD_HHMMSS format (IST assumption)"""
    return datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")

def resolve_csv_path():
    paths = [
        "/home/ubuntu/central_server/data/traffic_logs.csv",
        os.path.join(os.path.dirname(__file__), "..", "data", "traffic_logs.csv"),
        os.path.join(os.path.dirname(__file__), "traffic_logs.csv")
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def test_student_code(solution_path, vm_tag="DEFAULT"):
    problem_code = "pandas_server_traffic_logs"
    
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
    report_items = []
    total_score = 0
    fail_count = 0

    # Wrap the entire execution in a global try/except to guarantee report generation
    try:
        csv_file = resolve_csv_path()

        try:
            spec = importlib.util.spec_from_file_location("student_solution", solution_path)
            student_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(student_module)
        except Exception as e:
            err_detail = f"IMPORT ERROR: Failed to load TrafficAnalyzer: {e}\n{traceback.format_exc()}"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(err_detail + "\n")
            print(err_detail)
            return

        # Always use a guaranteed correct in-memory DataFrame to isolate logic test cases from CSV file loading/correctness issues
        try:
            raw_df = pd.DataFrame({
                'Timestamp': [
                    '2024-01-15 10:05:10', '2024-01-15 10:05:11', '2024-01-15 10:05:12', '2024-01-15 10:05:13',
                    '2024-01-15 10:05:14', '2024-01-15 10:05:15', '2024-01-15 10:05:16', '2024-01-15 10:05:17',
                    '2024-01-15 10:05:18', '2024-01-15 10:05:19', '2024-01-15 10:05:20', '2024-01-15 10:05:21',
                    '2024-01-15 10:05:22', '2024-01-15 10:05:23', '2024-01-15 10:05:24', '2024-01-15 10:05:25',
                    '2024-01-15 10:05:26', '2024-01-15 10:05:27', '2024-01-15 10:05:28', '2024-01-15 10:05:29'
                ],
                'Endpoint': [
                    '/api/users', '/profile', '/api/posts', '/profile', '/api/users', '/search', '/profile',
                    '/api/posts', '/api/users', '/search', '/profile', '/api/users', '/api/posts', '/search',
                    '/profile', '/api/users', '/api/posts', '/search', '/api/users', '/profile'
                ],
                'StatusCode': [200, 200, 200, 200, 200, 200, 200, 404, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 404, 200],
                'ResponseTime': [0.35, 0.92, 0.45, np.nan, 0.28, 0.67, 0.95, np.nan, 0.33, 0.71, 0.89, 0.31, 0.48, 0.65, 0.98, 0.36, 0.52, 12.5, 0.29, 15.2],
                'RequestSize': [1024, 512, 2048, 256, 1024, 512, 128, 1024, 2048, 256, 512, 1024, 2048, 512, 256, 1024, 2048, 512, 256, 1024],
                'ResponseSize': [2048, 1024, 4096, 512, 2048, 8192, 256, 128, 4096, 4096, 1024, 2048, 4096, 8192, 512, 2048, 4096, 8192, 128, 2048]
            })
            sanitized_df = raw_df[(raw_df['ResponseTime'] <= 10.0) | (raw_df['ResponseTime'].isna())].copy()
            fixed_df = sanitized_df.copy()
            mean_rt = fixed_df['ResponseTime'].mean()
            fixed_df['ResponseTime'] = fixed_df['ResponseTime'].fillna(mean_rt)
        except Exception as e:
            print(f"ERROR: Failed to initialize reference datasets: {e}")
            return

        if not csv_file:
            csv_file = "traffic_logs.csv"

        test_cases = [
            ("Load traffic_logs.csv and verify 20 rows loaded", "read_logs", 2),
            ("Identify and remove 2 outliers (ResponseTime > 10s)", "sanitize_latency", 3),
            ("Verify 18 rows remain after outlier removal", "sanitize_latency", 2),
            ("Fill NaN values in ResponseTime with mean", "fix_missing_records", 3),
            ("Identify slowest endpoint (/profile with ~0.93s avg)", "get_slowest_endpoint", 3),
            ("Count 404 errors in traffic logs", "count_errors", 3),
            ("Check for 500 errors (should return 0)", "count_errors", 2),
            ("Verify row count is correct after all operations", "fix_missing_records", 2)
        ]
        
        total_tc = len(test_cases)
        print(f"Running Evaluation for: {problem_code}\n")
        print(f"{'Test Case':<15} | {'Status':<10} | {'Marks'}")
        print("-" * 50)
        
        random.seed(None)
        for i, (desc, func_name, marks) in enumerate(test_cases, 1):
            try:
                def run_t(case_idx, current_obj, current_df=None):
                    if case_idx == 1:
                        current_obj.read_logs(csv_file)
                        return len(current_obj.df) if current_obj.df is not None else 0
                    if case_idx == 2:
                        if current_df is not None: current_obj.df = current_df.copy()
                        return current_obj.sanitize_latency()
                    if case_idx == 3:
                        if current_df is not None: current_obj.df = current_df.copy()
                        current_obj.sanitize_latency()
                        return len(current_obj.df) if current_obj.df is not None else 0
                    if case_idx == 4:
                        if current_df is not None: current_obj.df = current_df.copy()
                        current_obj.fix_missing_records()
                        return current_obj.df['ResponseTime'].isna().sum() if current_obj.df is not None else 0
                    if case_idx == 5:
                        if current_df is not None: current_obj.df = current_df.copy()
                        return current_obj.get_slowest_endpoint()
                    if case_idx == 6:
                        if current_df is not None: current_obj.df = current_df.copy()
                        return current_obj.count_errors(404)
                    if case_idx == 7:
                        if current_df is not None: current_obj.df = current_df.copy()
                        return current_obj.count_errors(500)
                    if case_idx == 8:
                        if current_df is not None: current_obj.df = current_df.copy()
                        current_obj.sanitize_latency()
                        current_obj.fix_missing_records()
                        return len(current_obj.df) if current_obj.df is not None else 0
                    return None

                obj = student_module.TrafficAnalyzer()
                
                # Check for pass-only implementation
                func = getattr(obj, func_name)
                src = inspect.getsource(func).replace(" ", "").replace("\n", "").lower()
                if 'pass' in src and len(src) < 80:
                    msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Contains only 'pass'"
                    results.append(msg)
                    print(f"TC{i:02d} [{desc[:30]:<30}] | FAILED     | 0/{marks}")
                    continue

                # Run test case
                p_ok = False
                if i == 1:
                    res = run_t(i, obj)
                    exp = 20
                elif i == 2:
                    res = run_t(i, obj, raw_df)
                    exp = 2
                elif i == 3:
                    res = run_t(i, obj, raw_df)
                    exp = 18
                elif i == 4:
                    res = run_t(i, obj, sanitized_df)
                    exp = 0
                elif i == 5:
                    res = run_t(i, obj, fixed_df)
                    exp = "/profile"
                elif i == 6:
                    res = run_t(i, obj, raw_df)
                    exp = 2
                elif i == 7:
                    res = run_t(i, obj, raw_df)
                    exp = 0
                elif i == 8:
                    res = run_t(i, obj, raw_df)
                    exp = 18
                    
                if res == exp:
                    p_ok = True

                tc_name = f"TC{i} [{desc}]"
                report_items.append(f"TC{i} (Visible)")
                
                if p_ok:
                    total_score += marks
                    status = "PASSED"
                    results.append(f"✓ {tc_name}: PASSED ({marks})")
                else:
                    status = "FAILED"
                    fail_count += 1
                    results.append(f"✗ {tc_name}: FAILED (0/{marks}) | Incorrect Output. Expected: {exp} | Actual: {res}")
                    
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
        if arg1.endswith(".py") or "/" in arg1 or "\\" in arg1 or os.path.exists(arg1):
            sol = os.path.abspath(arg1)
            vm = arg2 if arg2 else "DEFAULT"
        else:
            vm = arg1
            sol = os.path.abspath(arg2) if arg2 else os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    else:
        vm = "DEFAULT"
        sol = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol, vm)
