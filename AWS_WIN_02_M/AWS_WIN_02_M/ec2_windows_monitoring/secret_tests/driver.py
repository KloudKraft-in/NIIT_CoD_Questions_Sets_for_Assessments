import json
import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta

# Capture Assessment Start Time
START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', 'LOCAL_USER')

def resolve_username(default_prefix):
    return default_prefix

def verify_task():
    username = resolve_username(USER_PREFIX)
    start_time = START_TIME_STR

    print("\n" + "-" * 60)
    print(f"{'NIIT WINDOWS MONITORING VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}

    try:
        session_start = START_TIME
        if not session_start:
            session_start = datetime.now(timezone.utc)
            start_time = session_start.isoformat()

        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - session_start).total_seconds() / 60
        max_duration_env = os.getenv('NIIT_ASSESSMENT_DURATION') or os.getenv('NIIT_ASSESSMENT_DURATION')
        max_duration = int(max_duration_env) if max_duration_env else 60

        if elapsed_minutes > max_duration + 10:
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating Local Windows Environment for: {username}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        # Helper to execute PowerShell scripts locally
        def run_powershell(cmd):
            try:
                output = subprocess.check_output(["powershell", "-Command", cmd], text=True, stderr=subprocess.STDOUT)
                return True, output.strip()
            except subprocess.CalledProcessError as e:
                return False, e.output.strip()

        # --- TC1: Local Environment Verification --- (0 Marks)
        tc1_passed = True
        print(f"TC1: Local Environment Verification .............. [PASSED] (0/0)")
        results['tc1'] = tc1_passed
        total_score += 0

        # --- TC2: Service Management (IIS) --- (4 Marks)
        tc2_passed = False
        cmd = "(Get-Service w3svc -ErrorAction SilentlyContinue).Status -eq 'Running'"
        success, output = run_powershell(cmd)
        if success and "True" in output:
            tc2_passed = True
            print(f"TC2: Service Management (IIS) .................... [PASSED] (4/4)")
        else:
            print(f"TC2: Service Management (IIS) .................... [FAILED] (0/4)")
            print(f"     - [Reason]: IIS service 'W3SVC' is not running or not installed.")
        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 4

        # --- TC3: Automated Monitoring (Scheduled Task) --- (4 Marks)
        tc3_passed = False
        cmd = "[bool](Get-ScheduledTask -TaskName 'MemoryMonitorTask' -ErrorAction SilentlyContinue)"
        success, output = run_powershell(cmd)
        if success and "True" in output:
            tc3_passed = True
            print(f"TC3: Automated Monitoring (Scheduled Task) ....... [PASSED] (4/4)")
        else:
            print(f"TC3: Automated Monitoring (Scheduled Task) ....... [FAILED] (0/4)")
            print(f"     - [Reason]: Scheduled Task 'MemoryMonitorTask' does not exist.")
        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 4

        # Helper to check if file exists and is not empty
        def check_file(filepath):
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    return len(f.read().strip()) > 0
            return False

        # --- TC4: Disk Utilization Report --- (4 Marks)
        tc4_passed = False
        if check_file('C:\\workspace\\monitor\\disk_report.txt'):
            tc4_passed = True
            print(f"TC4: Disk Utilization Report ..................... [PASSED] (4/4)")
        else:
            print(f"TC4: Disk Utilization Report ..................... [FAILED] (0/4)")
            print(f"     - [Reason]: disk_report.txt is missing or empty.")
        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 4

        # --- TC5: CPU Process Monitoring --- (4 Marks)
        tc5_passed = False
        if check_file('C:\\workspace\\monitor\\cpu_process_report.txt'):
            tc5_passed = True
            print(f"TC5: CPU Process Monitoring ...................... [PASSED] (4/4)")
        else:
            print(f"TC5: CPU Process Monitoring ...................... [FAILED] (0/4)")
            print(f"     - [Reason]: cpu_process_report.txt is missing or empty.")
        results['tc5'] = tc5_passed
        if tc5_passed:
            total_score += 4

        # --- TC6: Network & Event Log Diagnostics --- (4 Marks)
        tc6_passed = False
        if check_file('C:\\workspace\\monitor\\network_status.txt') and check_file('C:\\workspace\\monitor\\event_errors.txt'):
            tc6_passed = True
            print(f"TC6: Network & Event Log Diagnostics ............. [PASSED] (4/4)")
        else:
            print(f"TC6: Network & Event Log Diagnostics ............. [FAILED] (0/4)")
            print(f"     - [Reason]: network_status.txt or event_errors.txt is missing or empty.")
        results['tc6'] = tc6_passed
        if tc6_passed:
            total_score += 4

        print("-" * 60)
        print(f"{'TOTAL SCORE:':<44} {total_score}/20")
        print("-" * 60 + "\n")

    except Exception as e:
        print(f"[ERROR] Verification failed: {str(e)}")
        total_score = 0

    # Save Metadata for Central Evaluation
    solution_data = {
        'candidate_prefix': username,
        'assessment_start_time': start_time,
        'max_duration_minutes': max_duration,
        'evaluation_type': 'LOCAL_VM_VERIFICATION',
        'score': total_score,
        'results': results
    }

    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        
        sol_path = os.path.join(ws_path, 'solution.json')
        existing_data = {}
        if os.path.exists(sol_path):
            try:
                with open(sol_path, 'r') as f:
                    existing_data = json.load(f)
            except Exception: pass
        
        existing_data.update(solution_data)
        
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
            json.dump(existing_data, f, indent=4)
        with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
            json.dump(existing_data, f, indent=4)
            
        root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
            json.dump(existing_data, f, indent=4)
        with open(os.path.join(root_ws_path, 'solution.py'), 'w') as f:
            json.dump(existing_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == "__main__":
    verify_task()
