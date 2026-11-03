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
    print(f"{'NIIT WINDOWS BASICS VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}
    
    def check_mtime(path):
        if not START_TIME:
            return True
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
            return mtime >= START_TIME - timedelta(minutes=5)
        except Exception:
            return False

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

        # --- TC1: Local Environment Verification --- (0 Marks)
        tc1_passed = True
        print(f"TC1: Local Environment Verification .............. [PASSED] (0/0)")
        results['tc1'] = tc1_passed
        total_score += 0

        # --- TC2: Logs Directory Structure --- (4 Marks)
        tc2_passed = False
        if os.path.isdir('C:\\workspace\\logs') and check_mtime('C:\\workspace\\logs'):
            tc2_passed = True
            print(f"TC2: Logs Directory Structure .................... [PASSED] (4/4)")
        else:
            print(f"TC2: Logs Directory Structure .................... [FAILED] (0/4)")
            print(f"     - [Reason]: Directory 'C:\\workspace\\logs' does not exist or was created before the session started.")
        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 4

        # --- TC3: Backups Directory Structure --- (4 Marks)
        tc3_passed = False
        if os.path.isdir('C:\\workspace\\backups') and check_mtime('C:\\workspace\\backups'):
            tc3_passed = True
            print(f"TC3: Backups Directory Structure ................. [PASSED] (4/4)")
        else:
            print(f"TC3: Backups Directory Structure ................. [FAILED] (0/4)")
            print(f"     - [Reason]: Directory 'C:\\workspace\\backups' does not exist or was created before the session started.")
        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 4

        # --- TC4: System Environment Variables --- (4 Marks)
        tc4_passed = False
        try:
            # PowerShell command to get the Machine-level environment variable
            cmd = "[Environment]::GetEnvironmentVariable('APP_ENVIRONMENT', 'Machine')"
            output = subprocess.check_output(["powershell", "-Command", cmd], text=True).strip()
            if output == "production":
                tc4_passed = True
                print(f"TC4: System Environment Variables ................ [PASSED] (4/4)")
            else:
                print(f"TC4: System Environment Variables ................ [FAILED] (0/4)")
                print(f"     - [Reason]: Permanent system-level variable 'APP_ENVIRONMENT' is not set to 'production'. Found: '{output}'")
        except Exception as e:
            print(f"TC4: System Environment Variables ................ [FAILED] (0/4)")
            print(f"     - [Reason]: Failed to check environment variable. Error: {e}")
        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 4

        # --- TC5: System Metadata --- (4 Marks)
        tc5_passed = False
        sysinfo_path = 'C:\\workspace\\sysinfo.txt'
        if os.path.isfile(sysinfo_path) and check_mtime(sysinfo_path):
            with open(sysinfo_path, 'r', encoding='utf-8', errors='ignore') as f1:
                if len(f1.read().strip()) > 0:
                    tc5_passed = True
                    print(f"TC5: System Metadata ............................. [PASSED] (4/4)")
                else:
                    print(f"TC5: System Metadata ............................. [FAILED] (0/4)")
                    print(f"     - [Reason]: File 'sysinfo.txt' is empty.")
        else:
            print(f"TC5: System Metadata ............................. [FAILED] (0/4)")
            print(f"     - [Reason]: 'sysinfo.txt' not found or was modified before the session started.")
        results['tc5'] = tc5_passed
        if tc5_passed:
            total_score += 4

        # --- TC6: Log Auditing --- (4 Marks)
        tc6_passed = False
        log_files_path = 'C:\\workspace\\log_files.txt'
        if os.path.isfile(log_files_path) and check_mtime(log_files_path):
            with open(log_files_path, 'r', encoding='utf-8', errors='ignore') as f2:
                if len(f2.read().strip()) > 0:
                    tc6_passed = True
                    print(f"TC6: Log Auditing ................................ [PASSED] (4/4)")
                else:
                    print(f"TC6: Log Auditing ................................ [FAILED] (0/4)")
                    print(f"     - [Reason]: File 'log_files.txt' is empty.")
        else:
            print(f"TC6: Log Auditing ................................ [FAILED] (0/4)")
            print(f"     - [Reason]: 'log_files.txt' not found or was modified before the session started.")
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
