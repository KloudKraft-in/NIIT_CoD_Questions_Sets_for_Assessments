import json
import os
import sys
import tarfile
from datetime import datetime, timezone, timedelta

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
HOME = os.path.expanduser('~')

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'NIIT LOCAL LINUX VERIFICATION':^60}")
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

    # TC1: Local VM Environment active and verified
    tc1_passed = os.path.exists(HOME) and os.path.isdir(HOME)
    results['tc1'] = tc1_passed
    print(f"TC1: {'VM Environment Verification':<30} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: Network Connectivity (ping_results.txt)
    tc2_passed = False
    ping_file = os.path.join(HOME, 'ping_results.txt')
    if os.path.isfile(ping_file) and check_mtime(ping_file):
        try:
            with open(ping_file, 'r') as f:
                content = f.read()
                if "ping statistics" in content.lower() and "packets transmitted" in content.lower():
                    if "100% packet loss" not in content.lower():
                        tc2_passed = True
        except Exception:
            pass
    results['tc2'] = tc2_passed
    total_score += 4 if tc2_passed else 0
    print(f"TC2: {'Network Connectivity Log':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({4 if tc2_passed else 0}/4)")

    # TC3: Port Diagnostics (open_ports.txt)
    tc3_passed = False
    ports_file = os.path.join(HOME, 'open_ports.txt')
    if os.path.isfile(ports_file) and check_mtime(ports_file):
        try:
            with open(ports_file, 'r') as f:
                content = f.read()
                if "State" in content or "Local Address" in content or "Proto" in content or len(content.strip()) > 50:
                    tc3_passed = True
        except Exception:
            pass
    results['tc3'] = tc3_passed
    total_score += 4 if tc3_passed else 0
    print(f"TC3: {'Port Diagnostics Report':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({4 if tc3_passed else 0}/4)")

    # TC4: IP Configuration (ip_config.txt)
    tc4_passed = False
    ip_file = os.path.join(HOME, 'ip_config.txt')
    if os.path.isfile(ip_file) and check_mtime(ip_file):
        try:
            with open(ip_file, 'r') as f:
                content = f.read()
                if "inet " in content or "ether " in content or "lo:" in content or "eth0:" in content or "ens" in content:
                    tc4_passed = True
        except Exception:
            pass
    results['tc4'] = tc4_passed
    total_score += 4 if tc4_passed else 0
    print(f"TC4: {'IP Configuration Report':<30} [{'PASSED' if tc4_passed else 'FAILED'}] ({4 if tc4_passed else 0}/4)")

    # TC5: Dummy log file creation
    tc5_passed = False
    log_file = os.path.join(HOME, 'dummy_app.log')
    if os.path.isfile(log_file) and check_mtime(log_file):
        tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 4 if tc5_passed else 0
    print(f"TC5: {'Dummy Log File Creation':<30} [{'PASSED' if tc5_passed else 'FAILED'}] ({4 if tc5_passed else 0}/4)")

    # TC6: File Compression (app_archive.tar.gz contains dummy_app.log)
    tc6_passed = False
    archive_file = os.path.join(HOME, 'app_archive.tar.gz')
    if os.path.isfile(archive_file) and check_mtime(archive_file):
        try:
            with tarfile.open(archive_file, 'r:gz') as tar:
                names = tar.getnames()
                if any("dummy_app.log" in name for name in names):
                    tc6_passed = True
        except Exception:
            pass
    results['tc6'] = tc6_passed
    total_score += 4 if tc6_passed else 0
    print(f"TC6: {'Tarball Archive Compression':<30} [{'PASSED' if tc6_passed else 'FAILED'}] ({4 if tc6_passed else 0}/4)")

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
    
    with open(sol_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

if __name__ == "__main__":
    verify_task()
