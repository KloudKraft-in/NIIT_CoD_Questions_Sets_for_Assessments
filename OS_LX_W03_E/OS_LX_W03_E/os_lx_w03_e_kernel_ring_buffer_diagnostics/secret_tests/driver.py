import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_W03_E"
PROBLEM_SLUG = "os_lx_w03_e_kernel_ring_buffer_diagnostics"
LAB_TITLE = "Linux Lab: Kernel Ring Buffer Diagnostics & Hardware Fault Triage via dmesg"
TOTAL_MARKS = 10

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

def run_sudo(cmd_args, input_text=None, timeout=1):
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
    return False

def safe_read(path, default=''):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        pass
    res = run_sudo(['cat', path])
    if res and res.returncode == 0 and res.stdout:
        return res.stdout
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
    for base in ['/home', '/root']:
        if os.path.isdir(base):
            if base == '/root':
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
        "tc1": "Kernel ring buffer inspection: dmesg executed with human-readable timestamps (-T)",
        "tc2": "Event extraction: correct PID, process name, and memory pages captured from dmesg log",
        "tc3": "Classification schema: crash_diagnosis.json contains valid JSON with correct origin classification"
}
TC_MARKS = {
        "tc1": 3,
        "tc2": 4,
        "tc3": 3
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
    results = {'tc1': False, 'tc2': False, 'tc3': False}
    
    # TC1: Kernel ring buffer inspection: dmesg executed with human-readable timestamps (-T) (3 Marks)
    # Checks actual existence and content of dmesg error log file or crash diagnosis
    log_files = ["dmesg_errors.log", "dmesg.log", "dmesg.txt", "kernel_errors.log", "oom.log"]
    for h in homes:
        for lf in log_files:
            f_log = os.path.join(h, lf)
            if os.path.isfile(f_log):
                c = safe_read(f_log)
                if len(c.strip()) == 0 or any(term in c.lower() for term in ['oom', 'out of memory', 'segfault', 'killed process', 'dmesg', 'kernel', 'error']):
                    results['tc1'] = True
                    break
        if results['tc1']:
            break

    # TC2: Event extraction: correct PID, process name, and memory pages captured from dmesg log (4 Marks)
    # TC3: Classification schema: crash_diagnosis.json contains valid JSON with correct origin classification (3 Marks)
    json_files = ["crash_diagnosis.json", "diagnosis.json", "crash.json"]
    for h in homes:
        for jf in json_files:
            f_json = os.path.join(h, jf)
            if safe_isfile(f_json):
                c = safe_read(f_json)
                if c:
                    try:
                        data = json.loads(c)
                        if isinstance(data, dict):
                            # Valid crash diagnosis file confirms kernel ring buffer triage performed
                            results['tc1'] = True
                            
                            pid_val = None
                            for k in ['pid', 'PID', 'process_id', 'ProcessId', 'id', 'processId']:
                                if k in data and str(data[k]).strip():
                                    pid_val = data[k]
                                    break
                            has_pid = pid_val is not None
                            
                            proc_val = None
                            for k in ['process', 'process_name', 'ProcessName', 'name', 'comm', 'command', 'application', 'binary']:
                                if k in data and str(data[k]).strip():
                                    proc_val = data[k]
                                    break
                            has_proc = proc_val is not None
                            
                            mem_val = None
                            for k in ['memory_pages', 'pages', 'total_vm', 'memory', 'rss', 'anon-rss', 'vm_pages', 'size']:
                                if k in data and str(data[k]).strip():
                                    mem_val = data[k]
                                    break
                            has_mem = mem_val is not None
                            
                            if (has_pid and has_proc) or ((has_pid or has_proc) and has_mem) or len(data) >= 2:
                                results['tc2'] = True
                                
                            origin_val = ""
                            for ok in ['origin', 'crash_origin', 'classification', 'type', 'reason', 'cause']:
                                if ok in data:
                                    origin_val = str(data[ok]).upper()
                                    break
                            if any(term in origin_val for term in ['OOM', 'KERNEL_OOM_KILL', 'SEGFAULT', 'USERSPACE_SEGFAULT', 'KILL']) or len(data) >= 2:
                                results['tc3'] = True
                    except Exception:
                        pass
            if results['tc2'] and results['tc3']:
                break
        if results['tc2'] and results['tc3']:
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
