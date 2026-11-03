import importlib.util
import os
import inspect
import numpy as np
import pandas as pd
import warnings

# Suppress all pandas/setting-with-copy warnings to prevent console stderr coloring
warnings.filterwarnings("ignore")

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

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(student_module)
    except Exception as e:
        print(f"IMPORT ERROR: {e}")
        return

    print("Running Tests for: Server Traffic Logs Analysis\n")
    report_lines = ["Running Tests for: Server Traffic Logs Analysis\n"]

    csv_file = resolve_csv_path()
    
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

    total_score = 0
    for idx, (desc, func_name, marks) in enumerate(test_cases, 1):
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
                msg = f"FAIL TC{idx} [{desc}] (0/{marks}) - Contains only 'pass'"
                report_lines.append(msg)
                print(msg)
                continue

            # Run test case
            p_ok = False
            if idx == 1:
                res = run_t(idx, obj)
                exp = 20
            elif idx == 2:
                res = run_t(idx, obj, raw_df)
                exp = 2
            elif idx == 3:
                res = run_t(idx, obj, raw_df)
                exp = 18
            elif idx == 4:
                res = run_t(idx, obj, sanitized_df)
                exp = 0
            elif idx == 5:
                res = run_t(idx, obj, fixed_df)
                exp = "/profile"
            elif idx == 6:
                res = run_t(idx, obj, raw_df)
                exp = 2
            elif idx == 7:
                res = run_t(idx, obj, raw_df)
                exp = 0
            elif idx == 8:
                res = run_t(idx, obj, raw_df)
                exp = 18
                
            if res == exp:
                p_ok = True

            if p_ok:
                total_score += marks
                msg = f"PASS TC{idx} [{desc}] ({marks})"
            else:
                msg = f"FAIL TC{idx} [{desc}] (0/{marks}) - Incorrect Output. Expected: {exp} | Actual: {res}"
            
            print(msg)
            report_lines.append(msg)

        except Exception as e:
            msg = f"FAIL TC{idx} [{desc}] (0/{marks}) - Error: {str(e)}"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/20.0"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
