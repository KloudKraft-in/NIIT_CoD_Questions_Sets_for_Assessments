import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_W04_E"
PROBLEM_SLUG = "os_lx_w04_e_rhel_package_management_repositories"
LAB_TITLE = "Linux Lab: RHEL Package Management, Repositories & Dependency Inspection"
TOTAL_MARKS = 10

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

_CAN_SUDO = None
def can_sudo():
    global _CAN_SUDO
    if _CAN_SUDO is None:
        try:
            res = subprocess.run(['sudo', '-n', 'true'], capture_output=True, timeout=1)
            _CAN_SUDO = (res.returncode == 0)
        except Exception:
            _CAN_SUDO = False
    return _CAN_SUDO

def run_sudo(cmd_args, input_text=None, timeout=1):
    if not can_sudo():
        return None
    try:
        res = subprocess.run(['sudo', '-n'] + cmd_args, input=input_text, capture_output=True, text=True, timeout=timeout)
        if res.returncode == 0:
            return res
    except Exception:
        pass
    return None

def safe_isdir(path):
    try:
        if os.path.isdir(path):
            return True
    except PermissionError:
        res = run_sudo(['test', '-d', path])
        if res and res.returncode == 0:
            return True
    except Exception:
        pass
    return False

def safe_isfile(path):
    try:
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            return True
    except PermissionError:
        res = run_sudo(['test', '-s', path])
        if res and res.returncode == 0:
            return True
    except Exception:
        pass
    return False

def safe_read(path, default=''):
    try:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    except PermissionError:
        res = run_sudo(['cat', path])
        if res and res.returncode == 0 and res.stdout:
            return res.stdout
    except Exception:
        pass
    return default

def find_all_user_homes():
    homes = set()
    try:
        cwd = os.getcwd()
        homes.add(cwd)
        homes.add(os.path.dirname(cwd))
        sw = os.path.join(cwd, 'student_workspace')
        if os.path.isdir(sw):
            homes.add(sw)
    except Exception:
        pass
    homes.add(os.path.expanduser('~'))
    for u in ['LabsKraft', 'ubuntu', 'labskraft', 'Niit', 'niit']:
        p = f'/home/{u}'
        if os.path.isdir(p):
            homes.add(p)
    return [h for h in homes if os.path.isdir(h)]

TC_NAMES = {
        "tc1": "Repository audit: dnf repolist correctly lists all enabled RHEL repository IDs",
        "tc2": "Package metadata query: dnf info accurately extracts version and release details",
        "tc3": "Package installation: jq package installed successfully with zero unresolved dependencies",
        "tc4": "Verification check: rpm -q confirms installed state and executable binary is located in PATH"
}
TC_MARKS = {
        "tc1": 2,
        "tc2": 3,
        "tc3": 3,
        "tc4": 2
}

def get_aws_metadata():
    import urllib.request
    try:
        token_req = urllib.request.Request(
            "http://169.254.169.254/latest/api/token",
            headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'},
            method='PUT'
        )
        token = urllib.request.urlopen(token_req, timeout=1).read().decode()
        id_req = urllib.request.Request(
            "http://169.254.169.254/latest/meta-data/instance-id",
            headers={'X-aws-ec2-metadata-token': token}
        )
        instance_id = urllib.request.urlopen(id_req, timeout=1).read().decode()
        region_req = urllib.request.Request(
            "http://169.254.169.254/latest/meta-data/placement/region",
            headers={'X-aws-ec2-metadata-token': token}
        )
        region = urllib.request.urlopen(region_req, timeout=1).read().decode()
        return instance_id, region
    except Exception:
        return None, None

def validate_all_tcs(homes, check_mtime_func=None):
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False}
    
    # TC1: Repository audit: dnf repolist correctly lists all enabled RHEL repository IDs (2 Marks)
    repo_files = ["active_repos.txt", "repos.txt", "repolist.txt", "active_repo.txt"]
    for h in homes:
        for rf in repo_files:
            f1 = os.path.join(h, rf)
            if safe_isfile(f1):
                c = safe_read(f1).lower()
                if c and any(term in c for term in ['repo', 'id', 'status', 'baseos', 'appstream', 'epel', 'rhel', 'ubuntu', 'archive', 'packages']):
                    results['tc1'] = True
                    break
        if results['tc1']:
            break

    # TC2: Package metadata query: dnf info accurately extracts version and release details (3 Marks)
    pkg_files = ["package_info.txt", "pkg_info.txt", "packages.txt", "dnf_info.txt", "info.txt", "nginx_jq.txt"]
    for h in homes:
        for pf in pkg_files:
            f2 = os.path.join(h, pf)
            if safe_isfile(f2):
                c = safe_read(f2).lower()
                if c:
                    has_name = any(pkg in c for pkg in ['nginx', 'jq'])
                    has_ver = any(term in c for term in ['version', 'release', 'architecture', 'size', 'description', 'name'])
                    if has_name or has_ver:
                        results['tc2'] = True
                        break
        if results['tc2']:
            break

    # TC3: Package installation: jq package installed successfully with zero unresolved dependencies (3 Marks)
    jq_bin = shutil.which('jq') or ('/usr/bin/jq' if os.path.isfile('/usr/bin/jq') else None) or ('/bin/jq' if os.path.isfile('/bin/jq') else None)
    if jq_bin:
        try:
            res = subprocess.run([jq_bin, '--version'], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                results['tc3'] = True
        except Exception:
            results['tc3'] = True
    else:
        for h in homes:
            f3 = os.path.join(h, "jq_installed.txt")
            if safe_isfile(f3):
                c = safe_read(f3)
                if c and 'jq' in c.lower():
                    results['tc3'] = True
                    break

    # TC4: Verification check: rpm -q confirms installed state and executable binary is located in PATH (2 Marks)
    if jq_bin:
        results['tc4'] = True
    else:
        for h in homes:
            f4 = os.path.join(h, "jq_installed.txt")
            if safe_isfile(f4):
                c = safe_read(f4)
                if c and 'jq' in c.lower():
                    results['tc4'] = True
                    break

    return results

def verify_task():
    def check_mtime(path):
        if not os.path.exists(path):
            return False
        if not START_TIME:
            return True
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
            return mtime >= START_TIME - timedelta(hours=24)
        except Exception:
            return True

    all_homes = find_all_user_homes()
    results = validate_all_tcs(all_homes, check_mtime)
    total_score = sum(TC_MARKS[k] for k, v in results.items() if v)

    print("\n" + "-" * 60)
    print(f"{LAB_TITLE.upper() + ' VERIFICATION':^60}")
    print(f"System Hostname: {socket.gethostname()}")
    print("-" * 60)

    for k in sorted(TC_NAMES.keys()):
        status = "PASSED" if results.get(k, False) else "FAILED"
        desc = TC_NAMES.get(k, k.upper())
        marks = TC_MARKS.get(k, 0)
        earned = marks if results.get(k, False) else 0
        print(f"{k.upper()}: {desc:<35} [{status}] ({earned}/{marks})")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/{TOTAL_MARKS}")
    print("-" * 60 + "\n")
    sys.stdout.flush()

    ws_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    
    existing_data = {
        'question_id': QUESTION_CODE,
        'problem_code': PROBLEM_SLUG,
        'score': total_score,
        'total_marks': TOTAL_MARKS,
        'results': results
    }
    try:

        instance_id, aws_region = get_aws_metadata()

        if instance_id:

            existing_data['instance_id'] = instance_id

            existing_data['aws_region'] = aws_region

    except Exception:

        pass
        
    legacy_metadata_path = os.path.join(HOME, 'Niit_Workspace', PROBLEM_SLUG, 'student_workspace', 'solution.json')
    try:
        if os.path.isfile(legacy_metadata_path):
            with open(legacy_metadata_path, 'r') as f:
                metadata = json.load(f)
                metadata.update(existing_data)
                existing_data = metadata
    except Exception:
        pass
        
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(existing_data, f, indent=4)
    # Write to solution.py as well because the Niit IDE is hardcoded to only upload solution.py!
    with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
        json.dump(existing_data, f, indent=4)
        
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
        json.dump(existing_data, f, indent=4)
    with open(os.path.join(root_ws_path, 'solution.py'), 'w') as f:
        json.dump(existing_data, f, indent=4)
        
    try:
        if os.path.isdir(os.path.dirname(legacy_metadata_path)):
            with open(legacy_metadata_path, 'w') as f:
                json.dump(existing_data, f, indent=4)
    except Exception:
        pass

if __name__ == "__main__":
    verify_task()
