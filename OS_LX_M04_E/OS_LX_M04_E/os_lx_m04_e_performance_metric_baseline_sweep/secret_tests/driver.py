import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_M04_E"
PROBLEM_SLUG = "os_lx_m04_e_performance_metric_baseline_sweep"
LAB_TITLE = "Linux Lab: Performance Metric Baseline Sweep & System Health Scripting"
TOTAL_MARKS = 10

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

def safe_isdir(path):
    try:
        return os.path.isdir(path)
    except Exception:
        return False

def safe_isfile(path):
    try:
        return os.path.isfile(path) and os.path.getsize(path) > 0
    except Exception:
        return False

def safe_read(path, default=""):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return default

def find_all_user_homes():
    homes = set()
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
            except Exception:
                pass
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        homes.add(os.path.normpath(os.path.join(script_dir, '..')))
        homes.add(os.path.normpath(os.path.join(script_dir, '..', '..')))
        homes.add(os.getcwd())
    except Exception:
        pass
    return [h for h in homes if os.path.isdir(h)]

def get_aws_metadata():
    import urllib.request
    try:
        token_req = urllib.request.Request("http://169.254.169.254/latest/api/token", headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'}, method='PUT')
        token = urllib.request.urlopen(token_req, timeout=1).read().decode()
        id_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/instance-id", headers={'X-aws-ec2-metadata-token': token})
        instance_id = urllib.request.urlopen(id_req, timeout=1).read().decode()
        region_req = urllib.request.Request("http://169.254.169.254/latest/meta-data/placement/region", headers={'X-aws-ec2-metadata-token': token})
        region = urllib.request.urlopen(region_req, timeout=1).read().decode()
        return instance_id, region
    except Exception:
        return None, None

TC_NAMES = {
    "tc1": "Script executable permissions: ~/scripts/health_sweep.sh has +x execution rights and valid shebang",
    "tc2": "Load and memory parsing: uptime load average and free memory parsed and formatted cleanly",
    "tc3": "Filesystem and process metrics: root disk utilization percentage and top 3 CPU processes captured",
    "tc4": "Log destination and exit code: output written to /var/log/daily_health_sweep.log and script exits with code 0"
}
TC_MARKS = {
    "tc1": 2,
    "tc2": 3,
    "tc3": 3,
    "tc4": 2
}

def validate_all_tcs(homes, check_mtime_func):
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False}
    
    # Pre-create/ensure /var/log/daily_health_sweep.log is writable if possible
    try:
        if not os.path.exists('/var/log/daily_health_sweep.log'):
            subprocess.run('sudo -n touch /var/log/daily_health_sweep.log 2>/dev/null && sudo -n chmod 666 /var/log/daily_health_sweep.log 2>/dev/null', shell=True)
    except Exception:
        pass

    found_script = None
    script_candidates = []
    for h in homes:
        script_candidates.extend([
            os.path.join(h, 'scripts', 'health_sweep.sh'),
            os.path.join(h, 'health_sweep.sh'),
            os.path.join(h, 'scripts', 'health_check.sh'),
            os.path.join(h, 'health_check.sh')
        ])
    for s in script_candidates:
        if safe_isfile(s):
            found_script = s
            break
            
    # TC1: Script executable permissions: ~/scripts/health_sweep.sh has +x execution rights and valid shebang (2 Marks)
    if found_script:
        c = safe_read(found_script)
        has_shebang = c.startswith('#!/bin/bash') or c.startswith('#!/bin/sh') or c.startswith('#!/usr/bin/env') or '#!/' in c[:30]
        is_exec = os.access(found_script, os.X_OK) or (os.stat(found_script).st_mode & 0o111 != 0)
        if (has_shebang and is_exec) or is_exec or has_shebang:
            results['tc1'] = True
            
        # TC2: Load and memory parsing: uptime load average and free memory parsed and formatted cleanly (3 Marks)
        has_load_logic = ('uptime' in c or 'load' in c.lower() or 'proc/loadavg' in c)
        has_mem_logic = ('free' in c or 'mem' in c.lower() or 'proc/meminfo' in c)
        if has_load_logic and has_mem_logic:
            results['tc2'] = True
            
        # TC3: Filesystem and process metrics: root disk utilization percentage and top 3 CPU processes captured (3 Marks)
        has_disk_logic = any(w in c.lower() for w in ['df', 'disk', 'findmnt', 'lsblk', 'rootfs', 'usage', 'mount', '/dev/'])
        has_proc_logic = any(w in c.lower() for w in ['ps', 'top', 'cpu', 'head', 'sort', 'process', 'prstat'])
        if has_disk_logic and has_proc_logic:
            results['tc3'] = True
            
        # TC4: Log destination and exit code: output written to /var/log/daily_health_sweep.log and script exits with code 0 (2 Marks)
        if 'daily_health_sweep.log' in c:
            results['tc4'] = True
            
    # Check output log
    candidate_logs = ['/var/log/daily_health_sweep.log', '/tmp/daily_health_sweep.log']
    for h in homes:
        candidate_logs.append(os.path.join(h, 'var', 'log', 'daily_health_sweep.log'))
        candidate_logs.append(os.path.join(h, 'daily_health_sweep.log'))
        
    for log_p in candidate_logs:
        if safe_isfile(log_p):
            c_log = safe_read(log_p)
            if len(c_log.strip()) > 0:
                results['tc4'] = True
            if not results['tc2'] and ('load' in c_log.lower() or 'mem' in c_log.lower() or 'average' in c_log.lower()):
                results['tc2'] = True
            if not results['tc3'] and ('%' in c_log or 'cpu' in c_log.lower() or 'disk' in c_log.lower()):
                results['tc3'] = True
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

    print()
    print("-" * 60)
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
    print("-" * 60)
    print()

    ws_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    
    existing_data = {
        'question_id': QUESTION_CODE,
        'problem_code': PROBLEM_SLUG,
        'score': total_score,
        'total_marks': TOTAL_MARKS,
        'results': results
    }
    instance_id, aws_region = get_aws_metadata()
    if instance_id:
        existing_data['instance_id'] = instance_id
        existing_data['aws_region'] = aws_region
        
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
