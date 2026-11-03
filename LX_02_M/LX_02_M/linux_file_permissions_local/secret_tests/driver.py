import json
import os
import sys
import pwd
from datetime import datetime, timezone, timedelta

import socket

HOME = os.path.expanduser('~')

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', 'LOCAL_USER')

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'NIIT LOCAL LINUX VERIFICATION':^60}")
    print(f"System Hostname: {socket.gethostname()}")
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

    # TC1: Environment active and verified
    tc1_passed = os.path.exists(HOME) and os.path.isdir(HOME)
    results['tc1'] = tc1_passed
    total_score += 0
    print(f"TC1: {'Local VM Environment active':<30} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: User appuser created successfully
    tc2_passed = False
    if tc1_passed:
        try:
            pwd.getpwnam('appuser')
            tc2_passed = True
        except KeyError:
            pass
    results['tc2'] = tc2_passed
    total_score += 4 if tc2_passed else 0
    print(f"TC2: {'User appuser created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({4 if tc2_passed else 0}/4)")

    # TC3: Directory created
    tc3_passed = False
    if tc1_passed:
        if os.path.isdir(f'{HOME}/secure_data'):
            if check_mtime(f'{HOME}/secure_data'):
                tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 4 if tc3_passed else 0
    print(f"TC3: {'Directory secure_data created':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({4 if tc3_passed else 0}/4)")

    # TC4: Files created
    tc4_passed = False
    if tc1_passed:
        if os.path.isfile(f'{HOME}/secure_data/passwords.txt') and os.path.isfile(f'{HOME}/secure_data/config.ini'):
            if check_mtime(f'{HOME}/secure_data/passwords.txt') and check_mtime(f'{HOME}/secure_data/config.ini'):
                tc4_passed = True
    results['tc4'] = tc4_passed
    total_score += 4 if tc4_passed else 0
    print(f"TC4: {'Files created':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({4 if tc4_passed else 0}/4)")

    # TC5: Proper permissions applied
    tc5_passed = False
    if tc1_passed:
        if os.path.isfile(f'{HOME}/secure_data/passwords.txt') and os.path.isfile(f'{HOME}/secure_data/config.ini'):
            if check_mtime(f'{HOME}/secure_data/passwords.txt') and check_mtime(f'{HOME}/secure_data/config.ini'):
                p_mode = oct(os.stat(f'{HOME}/secure_data/passwords.txt').st_mode & 0o777)
                c_mode = oct(os.stat(f'{HOME}/secure_data/config.ini').st_mode & 0o777)
                if p_mode == '0o400' and c_mode == '0o755':
                    tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 4 if tc5_passed else 0
    print(f"TC5: {'Proper permissions applied':<30} [{'PASSED' if tc5_passed else 'FAILED'}] ({4 if tc5_passed else 0}/4)")

    # TC6: Ownership configured correctly
    tc6_passed = False
    if tc1_passed:
        if os.path.isfile(f'{HOME}/secure_data/config.ini'):
            if check_mtime(f'{HOME}/secure_data/config.ini'):
                try:
                    owner = pwd.getpwuid(os.stat(f'{HOME}/secure_data/config.ini').st_uid).pw_name
                    if owner == 'appuser':
                        tc6_passed = True
                except KeyError:
                    pass
    results['tc6'] = tc6_passed
    total_score += 4 if tc6_passed else 0
    print(f"TC6: {'Ownership configured correctly':<30} [{'PASSED' if tc6_passed else 'FAILED'}] ({4 if tc6_passed else 0}/4)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    
    sol_path = os.path.join(ws_path, 'solution.json')
    existing_data = {}
    if os.path.exists(sol_path):
        try:
            with open(sol_path, 'r') as f:
                existing_data = json.load(f)
        except Exception: pass
    
    existing_data.update({'score': total_score, 'results': results})
    
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(existing_data, f, indent=4)
    with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
        json.dump(existing_data, f, indent=4)
        
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
        json.dump(existing_data, f, indent=4)
    with open(os.path.join(root_ws_path, 'solution.py'), 'w') as f:
        json.dump(existing_data, f, indent=4)

if __name__ == "__main__":
    verify_task()
