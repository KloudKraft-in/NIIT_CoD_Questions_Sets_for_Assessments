import json
import os
import sys
from datetime import datetime, timezone, timedelta
import subprocess

ist_offset = timezone(timedelta(hours=5, minutes=30))

def verify_task_central(username, start_time_str, exam_code="UNKNOWN", **kwargs):
    if not exam_code or exam_code == "UNKNOWN":
        exam_code = os.getenv("NIIT_EXAM_CODE") or os.getenv("EXAM_CODE") or os.getenv("exam_code") or "UNKNOWN"
    print(f"\n--- Central Validation for {username} ---")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(current_dir, 'driver.py')

    tc_names = {
        "tc1": "solution.json exists in student_workspace/",
        "tc2": "Conflicting branch name ('feature/login') identified",
        "tc3": "Conflict marker file ('auth.js') correctly identified"
    }
    marks_list = [3, 4, 3]
    
    results = {k: False for k in tc_names}
    
    pre_computed = False
    solution_path = kwargs.get('solution_path')

    if solution_path and os.path.exists(solution_path):
        try:
            with open(solution_path, 'r') as f:
                data = json.load(f)
                if 'results' in data:
                    results = data['results']
                    pre_computed = True
                    print("[SYSTEM] Successfully read local evaluation results from payload.")
        except Exception:
            pass

    if not pre_computed:
        try:
            python_cmd = 'python3' if not os.name == 'nt' else 'python'
            process = subprocess.run([python_cmd, driver_path, '--json'], capture_output=True, text=True, timeout=120)
            if process.returncode == 0:
                results = json.loads(process.stdout.strip())
                print("[SYSTEM] Successfully executed local driver.py")
            else:
                print("[SYSTEM] driver.py failed to execute.")
        except Exception as e:
            print(f"[SYSTEM] Error running driver.py: {str(e)}")

    total_score = 0
    for k, v in results.items():
        try:
            tc_num = int(k[2:])
            if v:
                total_score += marks_list[tc_num - 1]
        except Exception:
            pass

    print(f"EXAM CODE: {exam_code}")

    for tc, name in tc_names.items():
        passed = results.get(tc, False)
        status = "PASSED" if passed else "FAILED"
        display_name = f"{tc.upper()} [{name}]"
        print(f"{display_name} - {status}")

    print(f"TOTAL SCORE: {total_score}")

    date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
    file_timestamp = datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")
    problem_code = "bca_git_conflict"

    passed_cases = []
    failed_cases = []
    for tc, name in tc_names.items():
        try:
            tc_num = int(tc[2:])
            marks = marks_list[tc_num - 1]
        except Exception:
            marks = 0
            
        display_name = f"{tc.upper()} [{name}]"
        if results.get(tc, False):
            passed_cases.append(f"{display_name}: ({marks}/{marks})")
        else:
            failed_cases.append(f"{display_name}: (0/{marks})")

    passed_str = f"{len(passed_cases)}: {'; '.join(passed_cases)}" if passed_cases else "0"
    failed_str = f"{len(failed_cases)}: {'; '.join(failed_cases)}" if failed_cases else "0"

    csv_line = f"{date_str},{problem_code},{exam_code.upper()},{username},{file_timestamp},{passed_str},{failed_str},{total_score}"
    print(f"\n[REPORT_CSV]{csv_line}")
    return total_score, results

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "demo4@labskraft.com"
    start_time = sys.argv[2] if len(sys.argv) > 2 else datetime.now(ist_offset).strftime("%Y-%m-%dT%H:%M:%S")
    exam_code = sys.argv[3] if len(sys.argv) > 3 else "1123"
    verify_task_central(username, start_time, exam_code)
