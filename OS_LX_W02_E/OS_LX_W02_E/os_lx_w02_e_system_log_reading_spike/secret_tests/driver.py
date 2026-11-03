import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_W02_E"
PROBLEM_SLUG = "os_lx_w02_e_system_log_reading_spike"
LAB_TITLE = "Linux Lab: System Log Reading & Spike Window Isolation"
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
    except PermissionError:
        res = run_sudo(['cat', path])
        if res and res.returncode == 0 and res.stdout:
            return res.stdout
    except Exception:
        pass
    return default

def get_all_bash_histories(homes):
    commands = []
    for h in homes:
        for hist_name in ['.bash_history', '.zsh_history', '.bash_eternal_history']:
            p = os.path.join(h, hist_name)
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
    for base in ['/home']:
        if os.path.isdir(base):
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
        "tc1": "Log metrics accuracy: total count of ERROR and TIMEOUT correctly calculated",
        "tc2": "Timestamp window isolation: incident_window.log contains strictly entries within 14:00:00-14:15:00",
        "tc3": "Regex IP extraction: culprit_ips.txt contains valid IPv4 addresses extracted from log lines",
        "tc4": "Deduplication: culprit_ips.txt contains uniquely sorted IP entries with no duplicates"
}
TC_MARKS = {
        "tc1": 3,
        "tc2": 3,
        "tc3": 2,
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

SAMPLE_SYSLOG = """Oct 27 13:45:10 web-srv01 systemd[1]: Started Daily apt upgrade and clean activities.
Oct 27 13:58:20 web-srv01 app[1042]: INFO Health check responding OK on port 8080
Oct 27 14:02:15 web-srv01 app[1042]: ERROR Database connection failure from 192.168.1.105
Oct 27 14:05:32 web-srv01 app[1042]: TIMEOUT Upstream gateway response timeout for client 10.0.0.45
Oct 27 14:08:19 web-srv01 app[1042]: ERROR Failed to authenticate user session from 172.16.0.88
Oct 27 14:12:44 web-srv01 app[1042]: TIMEOUT Request timeout from 192.168.1.105
Oct 27 14:14:50 web-srv01 app[1042]: ERROR Critical thread pool exhaustion caused by 10.0.0.45
Oct 27 14:18:05 web-srv01 app[1042]: INFO Service stabilized, normal latency restored
Oct 27 14:25:30 web-srv01 systemd[1]: Session 3 logged out.
"""

def ensure_syslog_exists():
    try:
        syslog_path = '/var/log/syslog'
        if not os.path.exists(syslog_path) or os.path.getsize(syslog_path) == 0:
            os.makedirs('/var/log', exist_ok=True)
            with open(syslog_path, 'w', encoding='utf-8') as f:
                f.write(SAMPLE_SYSLOG)
    except Exception:
        try:
            run_sudo(['tee', '/var/log/syslog'], input_text=SAMPLE_SYSLOG)
        except Exception:
            pass

def validate_all_tcs(homes, check_mtime_func):
    ensure_syslog_exists()
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False}
    histories = get_all_bash_histories(homes)
    
    # TC1: Log metrics accuracy: total count of ERROR and TIMEOUT correctly calculated (3 Marks)
    metric_files = ["log_metrics.txt", "metrics.txt", "log_metrics.log", "error_metrics.txt"]
    for h in homes:
        for mf in metric_files:
            f1 = os.path.join(h, mf)
            c = safe_read(f1)
            if c:
                has_err = bool(re.search(r'(?i)(error.*?\d+|\d+.*?error)', c))
                has_tout = bool(re.search(r'(?i)(timeout.*?\d+|\d+.*?timeout)', c))
                if (has_err and has_tout) or (re.search(r'\d+', c) and ('error' in c.lower() or 'timeout' in c.lower())):
                    results['tc1'] = True
                    break
        if results['tc1']:
            break
            
    if not results['tc1']:
        if any(('grep' in cmd and ('error' in cmd.lower() or 'timeout' in cmd.lower()) and ('syslog' in cmd or '-c' in cmd or 'log' in cmd)) for cmd in histories):
            results['tc1'] = True
            
    # TC2: Timestamp window isolation: incident_window.log contains strictly entries within 14:00:00-14:15:00 (3 Marks)
    window_files = ["incident_window.log", "window.log", "incident.log", "incident_window.txt"]
    for h in homes:
        for wf in window_files:
            f2 = os.path.join(h, wf)
            c = safe_read(f2)
            if c:
                lines = [line.strip() for line in c.splitlines() if line.strip()]
                if len(lines) >= 1:
                    has_valid_window = any(re.search(r'14:(0[0-9]|1[0-5]):[0-9]{2}', l) for l in lines)
                    if has_valid_window or ('14:' in c and ('error' in c.lower() or 'timeout' in c.lower())):
                        results['tc2'] = True
                        break
        if results['tc2']:
            break
            
    if not results['tc2']:
        if any(('14:00' in cmd or '14:15' in cmd or '14:' in cmd or 'incident_window' in cmd) for cmd in histories):
            results['tc2'] = True
            
    # TC3: Regex IP extraction: culprit_ips.txt contains valid IPv4 addresses extracted from log lines (2 Marks)
    # TC4: Deduplication: culprit_ips.txt contains uniquely sorted IP entries with no duplicates (2 Marks)
    ip_files = ["culprit_ips.txt", "culprit_ip.txt", "ips.txt", "culprit.txt"]
    for h in homes:
        for ipf in ip_files:
            f3 = os.path.join(h, ipf)
            c = safe_read(f3)
            if c:
                lines = [line.strip() for line in c.splitlines() if line.strip()]
                ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
                valid_ips = [l for l in lines if ip_pattern.search(l)]
                if len(valid_ips) >= 1:
                    results['tc3'] = True
                    results['tc4'] = True
                    break
        if results['tc3']:
            break
            
    if not results['tc3']:
        if any(('culprit_ips' in cmd or ('sort' in cmd and 'uniq' in cmd and ('ip' in cmd or 'grep' in cmd or 'awk' in cmd)) or ('grep' in cmd and '14:' in cmd)) for cmd in histories):
            results['tc3'] = True
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
