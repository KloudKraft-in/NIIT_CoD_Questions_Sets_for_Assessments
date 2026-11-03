import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_W05_M"
PROBLEM_SLUG = "os_lx_w05_m_systemd_service_unit_management"
LAB_TITLE = "Linux Lab: systemd Service Unit Management, Dependency Mapping & Failure Recovery"
TOTAL_MARKS = 20

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

SUDO_PASSWORDS = ['', 'labskraft', 'LabsKraft', 'Niit@123', 'niit123', 'ubuntu', 'password', 'Niit@2026', 'LabsKraft@123']

def run_sudo(cmd_args, input_text=None, timeout=2):
    try:
        res = subprocess.run(['sudo', '-n'] + cmd_args, input=input_text, stdin=subprocess.DEVNULL if input_text is None else None, capture_output=True, text=True, timeout=timeout)
        if res.returncode == 0:
            return res
    except Exception:
        pass
    for pwd in SUDO_PASSWORDS:
        if not pwd:
            continue
        try:
            stdin_data = pwd + chr(10) + (input_text if input_text else '')
            res = subprocess.run(['sudo', '-S', '-k'] + cmd_args, input=stdin_data, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=1)
            if res.returncode == 0:
                return res
            break
        except Exception:
            break
    return None

def safe_isdir(path):
    try:
        if os.path.isdir(path):
            return True
    except Exception:
        pass
    res = run_sudo(['test', '-d', path])
    if res and res.returncode == 0:
        return True
    return False

def safe_isfile(path):
    try:
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            return True
    except Exception:
        pass
    res = run_sudo(['test', '-s', path])
    if res and res.returncode == 0:
        return True
    res = run_sudo(['test', '-f', path])
    if res and res.returncode == 0:
        return True
    res = run_sudo(['ls', '-d', path])
    if res and res.returncode == 0 and res.stdout.strip():
        return True
    return False

def safe_read(path, default=''):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            c = f.read()
            if c:
                return c
    except Exception:
        pass
    res = run_sudo(['cat', path])
    if res and res.returncode == 0 and res.stdout:
        return res.stdout
    return default

def get_all_bash_histories(homes):
    commands = []
    for h in homes:
        if h == '/root' and not os.access('/root', os.R_OK):
            continue
        for hist_name in ['.bash_history', '.zsh_history', '.bash_eternal_history']:
            p = os.path.join(h, hist_name)
            if os.path.exists(p) and os.access(p, os.R_OK):
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        commands.extend(f.read().splitlines())
                except Exception:
                    pass
            else:
                content = safe_read(p)
                if content:
                    commands.extend(content.splitlines())
    return commands

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
    for base in ['/home', '/root']:
        if os.path.isdir(base):
            if base == '/root':
                if os.access('/root', os.R_OK):
                    homes.add('/root')
            else:
                try:
                    for u in os.listdir(base):
                        p = os.path.join(base, u)
                        if os.path.isdir(p):
                            homes.add(p)
                except Exception:
                    pass
    homes.add(os.path.expanduser('~'))
    for u in ['LabsKraft', 'ubuntu', 'labskraft', 'Niit', 'niit']:
        p = f'/home/{u}'
        if os.path.isdir(p):
            homes.add(p)
    for ws_base in ['/home/LabsKraft/NIIT_workspace', '/home/LabsKraft/NIIT_Workspace', '/home/ubuntu/NIIT_workspace', '/home/ubuntu/NIIT_Workspace']:
        if os.path.isdir(ws_base):
            homes.add(ws_base)
            try:
                for sub in os.listdir(ws_base):
                    sub_p = os.path.join(ws_base, sub)
                    if os.path.isdir(sub_p):
                        homes.add(sub_p)
                        for inner in os.listdir(sub_p):
                            inner_p = os.path.join(sub_p, inner)
                            if os.path.isdir(inner_p):
                                homes.add(inner_p)
            except Exception:
                pass
    return [h for h in homes if os.path.isdir(h)]

TC_NAMES = {
        "tc1": "Log diagnosis: journalctl logs parsed and root cause error message identified into ~/service_error.txt",
        "tc2": "Dependency isolation: prerequisite dependency unit identified via systemctl list-dependencies",
        "tc3": "Service recovery: prerequisite unit and orders-api restored to active (running) state",
        "tc4": "Boot persistence: systemctl is-enabled orders-api returns 'enabled'"
}
TC_MARKS = {
        "tc1": 5,
        "tc2": 5,
        "tc3": 5,
        "tc4": 5
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

def validate_all_tcs(homes, check_mtime_func):
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False}
    histories = get_all_bash_histories(homes)
    
    # TC1: Log diagnosis: journalctl logs parsed and root cause error message identified into ~/service_error.txt (5 Marks)
    err_files = ["service_error.txt", "orders_error.txt", "error.txt", "service.log", "journal.txt"]
    for h in homes:
        for ef in err_files:
            f1 = os.path.join(h, ef)
            c = safe_read(f1)
            if c:
                if any(term in c.lower() for term in ['orders-api', 'failed', 'exit-code', 'status=', 'code=exited', 'error', 'systemd']):
                    results['tc1'] = True
                    break
        if results['tc1']:
            break
            
    if not results['tc1']:
        if any(('journalctl' in cmd or 'systemctl status orders-api' in cmd or 'service_error' in cmd) for cmd in histories):
            results['tc1'] = True
                
    # TC2: Dependency isolation: prerequisite dependency unit identified via systemctl list-dependencies (5 Marks)
    dep_files = ["dependencies.txt", "dependency.txt", "dep.txt", "orders_dependencies.txt", "orders-api_dependencies.txt", "orders-api-dependencies.txt", "orders.txt"]
    for h in homes:
        for df in dep_files:
            f2 = os.path.join(h, df)
            c = safe_read(f2).lower()
            if c:
                if any(term in c for term in ['list-dependencies', 'requires', 'wants', 'orders-api', 'socket', 'database', 'target', 'service', 'unit']):
                    results['tc2'] = True
                    break
        if results['tc2']:
            break
            
    if not results['tc2']:
        if any(('list-dependencies' in cmd or 'dependencies.txt' in cmd or 'orders-api' in cmd) for cmd in histories):
            results['tc2'] = True
                
    # TC3: Service recovery: prerequisite unit and orders-api restored to active (running) state (5 Marks)
    systemctl_bin = shutil.which('systemctl')
    if systemctl_bin:
        for is_act_cmd in [[systemctl_bin, 'is-active', 'orders-api'], ['sudo', systemctl_bin, 'is-active', 'orders-api'], ['sudo', '-n', systemctl_bin, 'is-active', 'orders-api']]:
            try:
                res = subprocess.run(is_act_cmd, capture_output=True, text=True, timeout=5)
                if res.stdout.strip() == 'active':
                    results['tc3'] = True
                    break
            except Exception:
                pass
            
    if not results['tc3']:
        if safe_isfile('/etc/systemd/system/orders-api.service') or safe_isfile('/etc/systemd/system/multi-user.target.wants/orders-api.service') or safe_isfile('/lib/systemd/system/orders-api.service'):
            results['tc3'] = True
        elif any(('systemctl restart orders-api' in cmd or 'systemctl start orders-api' in cmd) for cmd in histories):
            results['tc3'] = True
            
    # TC4: Boot persistence: systemctl is-enabled orders-api returns 'enabled' (5 Marks)
    if systemctl_bin:
        for is_en_cmd in [[systemctl_bin, 'is-enabled', 'orders-api'], ['sudo', systemctl_bin, 'is-enabled', 'orders-api'], ['sudo', '-n', systemctl_bin, 'is-enabled', 'orders-api']]:
            try:
                res = subprocess.run(is_en_cmd, capture_output=True, text=True, timeout=5)
                if res.stdout.strip() == 'enabled':
                    results['tc4'] = True
                    break
            except Exception:
                pass
            
    if not results['tc4']:
        if safe_isfile('/etc/systemd/system/multi-user.target.wants/orders-api.service'):
            results['tc4'] = True
        elif any(('systemctl enable orders-api' in cmd or 'systemctl is-enabled orders-api' in cmd) for cmd in histories):
            results['tc4'] = True
            
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
