import json
import os
import sys
from datetime import datetime, timezone, timedelta

# Capture Assessment Start Time
START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', 'LOCAL_USER')

# Fix encoding for Windows consoles printing emojis
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_home_dir():
    # Prioritize /home/ubuntu if it exists, otherwise fall back to Niit/niit or default ~
    for p in ['/home/ubuntu', '/home/Niit', '/home/niit', os.path.expanduser('~')]:
        if os.path.isdir(p):
            return p
    return os.path.expanduser('~')

HOME = get_home_dir()

def resolve_username(default_prefix):
    return default_prefix

def verify_task():
    username = resolve_username(USER_PREFIX)
    start_time = START_TIME_STR

    print("\n" + "-" * 60)
    print(f"{'NIIT USER NAVIGATION VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}

    workspace_dir = "/var/tmp/backup_workspace"
    initial_file = "/var/tmp/backup_workspace/meta_log.txt"
    target_file = os.path.join(HOME, "meta_backup.log")

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

        print(f"[SYSTEM] Validating Local Linux Environment for: {username}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        # --- TC1: Local Environment Verification --- (0 Marks)
        tc1_passed = os.path.exists(HOME) and os.path.isdir(HOME)
        print(f"TC1: Local Environment active .................... [PASSED] (0/0)")
        results['tc1'] = tc1_passed
        total_score += 0

        # --- TC2: Backup Workspace Directory Creation --- (2 Marks)
        tc2_passed = False
        if tc1_passed:
            if os.path.isdir(workspace_dir):
                if check_mtime(workspace_dir):
                    tc2_passed = True
        if tc2_passed:
            print(f"TC2: Backup workspace created .................... [PASSED] (2/2)")
        else:
            print(f"TC2: Backup workspace created .................... [FAILED] (0/2)")
            print(f"     - [Reason]: Directory '{workspace_dir}' does not exist.")
        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 2

        # --- TC3: Initial Log File Creation --- (2 Marks)
        tc3_passed = False
        if tc1_passed:
            if os.path.isfile(target_file) or os.path.isfile(initial_file):
                tc3_passed = True
        if tc3_passed:
            print(f"TC3: Initial log file processed .................. [PASSED] (2/2)")
        else:
            print(f"TC3: Initial log file processed .................. [FAILED] (0/2)")
            print(f"     - [Reason]: File 'meta_log.txt' is missing from workspace.")
        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 2

        # --- TC4: File Migration & Renaming --- (3 Marks)
        tc4_passed = False
        if tc1_passed:
            if os.path.isfile(target_file):
                if check_mtime(target_file):
                    tc4_passed = True
        if tc4_passed:
            print(f"TC4: File moved to meta_backup.log ............... [PASSED] (3/3)")
        else:
            print(f"TC4: File moved to meta_backup.log ............... [FAILED] (0/3)")
            print(f"     - [Reason]: Target file '{target_file}' does not exist.")
        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 3

        # --- TC5: Workspace Cleanup Verification --- (3 Marks)
        tc5_passed = False
        if tc1_passed and tc4_passed:
            if not os.path.exists(initial_file):
                tc5_passed = True
        if tc5_passed:
            print(f"TC5: Original file cleaned from workspace ........ [PASSED] (3/3)")
        else:
            print(f"TC5: Original file cleaned from workspace ........ [FAILED] (0/3)")
            print(f"     - [Reason]: File 'meta_log.txt' is still present inside workspace.")
        results['tc5'] = tc5_passed
        if tc5_passed:
            total_score += 3

        print("-" * 60)
        print(f"{'TOTAL SCORE:':<44} {total_score}/10")
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
