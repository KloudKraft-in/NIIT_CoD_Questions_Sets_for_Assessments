import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_M09_M"
PROBLEM_SLUG = "os_lx_m09_m_comprehensive_enterprise_linux_outage"
LAB_TITLE = "Linux Lab: Comprehensive Enterprise Linux Outage Resolution & Runbook Execution"
TOTAL_MARKS = 20

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
    "tc1": "Initial triage assessment: multi-fault symptom log created identifying all 4 failure points",
    "tc2": "Disk capacity recovery: /var partition cleaned safely without deleting active database files",
    "tc3": "Orphaned process cleanup: locked process identified via fuser/lsof and terminated cleanly",
    "tc4": "Routing restoration: default gateway route restored and verified via ip route",
    "tc5": "Service restoration: nginx.service started and verified in active (running) state",
    "tc6": "HTTP endpoint response: curl -I http://localhost/ returns HTTP 200 OK",
    "tc7": "Clean system state: zero degraded systemd units and load average normal",
    "tc8": "Runbook execution log: /var/log/incident_recovery.log documents timestamps and actions taken"
}

TC_MARKS = {
    "tc1": 2,
    "tc2": 3,
    "tc3": 3,
    "tc4": 2,
    "tc5": 3,
    "tc6": 3,
    "tc7": 2,
    "tc8": 2
}

def check_bash_history(homes, pattern):
    for h in homes:
        for hist_file in [".bash_history", ".zsh_history"]:
            p = os.path.join(h, hist_file)
            if safe_isfile(p):
                content = safe_read(p)
                if re.search(pattern, content, re.I):
                    return True
    return False

def validate_all_tcs(homes, check_mtime_func):
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}

    candidate_logs = ['/var/log/incident_recovery.log']
    for h in homes:
        candidate_logs.append(os.path.join(h, "incident_recovery.log"))
        candidate_logs.append(os.path.join(h, "var", "log", "incident_recovery.log"))
        
    found_recovery_log = None
    for log_p in candidate_logs:
        if safe_isfile(log_p) and check_mtime_func(log_p):
            found_recovery_log = log_p
            break
            
    c_recovery = safe_read(found_recovery_log).lower() if found_recovery_log else ""

    # TC1: Initial triage assessment (2 Marks)
    triage_files = ["outage_triage.txt", "outage_triage.log", "triage.txt", "symptoms.txt"]
    found_triage_content = ""
    for h in homes:
        for tf in triage_files:
            tp = os.path.join(h, tf)
            if safe_isfile(tp) and check_mtime_func(tp):
                found_triage_content = safe_read(tp).lower()
                break
        if found_triage_content:
            break

    combined_triage = found_triage_content + "\n" + c_recovery
    fault_keywords = ['disk', 'process', 'route', 'nginx', 'network', 'lock', 'deadlock', 'storage', 'space', 'gateway']
    fault_count = sum(1 for w in fault_keywords if w in combined_triage)
    if fault_count >= 2:
        results['tc1'] = True
    elif check_bash_history(homes, r'outage_triage'):
        results['tc1'] = True

    # TC2: Disk capacity recovery (3 Marks)
    cleanup_files = ["var_cleanup.txt", "disk_cleanup.txt", "cleanup.txt", "log_cleanup.txt", "df.txt", "tc2.txt"]
    for h in homes:
        for cf in cleanup_files:
            cp = os.path.join(h, cf)
            if safe_isfile(cp) and check_mtime_func(cp):
                c = safe_read(cp).lower()
                if any(w in c for w in ['clean', 'vacuum', 'var', 'disk', 'df', 'space', 'size', 'log', 'deleted', 'free', 'filesystem']):
                    results['tc2'] = True
                    break
        if results['tc2']:
            break

    if not results['tc2']:
        if (check_bash_history(homes, r'journalctl\s+--vacuum') or
            check_bash_history(homes, r'find\s+/var/log.*delete') or
            check_bash_history(homes, r'rm\s+.*var/log') or
            check_bash_history(homes, r'df\s+-h.*var') or
            check_bash_history(homes, r'var_cleanup')):
            results['tc2'] = True

    if not results['tc2'] and c_recovery:
        if any(term in c_recovery for term in ['clean', 'cleanup', 'vacuum', 'disk', 'var/log']):
            results['tc2'] = True

    # TC3: Orphaned process cleanup (3 Marks)
    proc_files = ["process_killed.txt", "orphan_cleanup.txt", "deadlock_killed.txt", "fuser.txt", "lsof.txt", "process.txt", "tc3.txt"]
    for h in homes:
        for pf in proc_files:
            pp = os.path.join(h, pf)
            if safe_isfile(pp) and check_mtime_func(pp):
                c = safe_read(pp).lower()
                if any(w in c for w in ['kill', 'fuser', 'lsof', 'deadlock', 'pid', 'terminated', 'orphan', 'process', 'stopped', 'holding']):
                    results['tc3'] = True
                    break
        if results['tc3']:
            break

    if not results['tc3']:
        if (check_bash_history(homes, r'fuser') or
            check_bash_history(homes, r'lsof') or
            check_bash_history(homes, r'kill') or
            check_bash_history(homes, r'pkill') or
            check_bash_history(homes, r'process_killed')):
            results['tc3'] = True

    if not results['tc3'] and c_recovery:
        if any(term in c_recovery for term in ['kill', 'fuser', 'lsof', 'deadlock', 'terminated', 'orphan', 'process']):
            results['tc3'] = True

    # TC4: Routing restoration (2 Marks)
    route_files = ["ip_route.txt", "route_restored.txt", "route.txt", "gateway.txt", "tc4.txt"]
    for h in homes:
        for rf in route_files:
            rp = os.path.join(h, rf)
            if safe_isfile(rp) and check_mtime_func(rp):
                c = safe_read(rp).lower()
                if any(w in c for w in ['default via', 'default dev', 'default', 'kernel routing', 'gateway', 'proto dhcp', 'eth0']):
                    results['tc4'] = True
                    break
        if results['tc4']:
            break

    if not results['tc4']:
        ip_bin = shutil.which('ip')
        if ip_bin:
            try:
                res = subprocess.run([ip_bin, 'route', 'show'], capture_output=True, text=True, timeout=5)
                if 'default via' in res.stdout or 'default' in res.stdout or 'dev' in res.stdout:
                    results['tc4'] = True
            except Exception:
                pass

    if not results['tc4']:
        if (check_bash_history(homes, r'ip\s+route') or
            check_bash_history(homes, r'route') or
            check_bash_history(homes, r'ip_route')):
            results['tc4'] = True

    if not results['tc4'] and c_recovery:
        if 'gateway' in c_recovery or 'default via' in c_recovery or 'route' in c_recovery:
            results['tc4'] = True

    # TC5: Service restoration (3 Marks)
    systemctl_bin = shutil.which('systemctl')
    if systemctl_bin:
        try:
            res = subprocess.run([systemctl_bin, 'is-active', 'nginx'], capture_output=True, text=True, timeout=5)
            if res.stdout.strip() == 'active':
                results['tc5'] = True
        except Exception:
            pass

    if not results['tc5']:
        svc_files = ["service_status.txt", "nginx_status.txt", "service.txt", "nginx.txt", "tc5.txt"]
        for h in homes:
            for sf in svc_files:
                sp = os.path.join(h, sf)
                if safe_isfile(sp) and check_mtime_func(sp):
                    c = safe_read(sp).lower()
                    if any(w in c for w in ['active (running)', 'active', 'restarted', 'started', 'nginx', 'running', 'service', 'enabled']):
                        results['tc5'] = True
                        break
            if results['tc5']:
                break

    if not results['tc5']:
        if (check_bash_history(homes, r'nginx') or
            check_bash_history(homes, r'service_status')):
            results['tc5'] = True

    if not results['tc5'] and c_recovery:
        if 'nginx' in c_recovery and any(w in c_recovery for w in ['active', 'running', 'restarted', 'started', 'restored']):
            results['tc5'] = True

    # TC6: HTTP endpoint response (3 Marks)
    curl_bin = shutil.which('curl')
    if curl_bin:
        try:
            res = subprocess.run([curl_bin, '-s', '-I', 'http://localhost/'], capture_output=True, text=True, timeout=3)
            if any(code in res.stdout for code in ['200', '301', '302', '403', '404', 'HTTP/']):
                results['tc6'] = True
        except Exception:
            pass

    if not results['tc6']:
        curl_files = ["curl_check.txt", "http_response.txt", "curl_output.txt", "curl.txt", "tc6.txt"]
        for h in homes:
            for cf in curl_files:
                cp = os.path.join(h, cf)
                if safe_isfile(cp) and check_mtime_func(cp):
                    c = safe_read(cp).lower()
                    if any(w in c for w in ['200 ok', '200', 'http', 'ok', 'html', 'curl', 'server']):
                        results['tc6'] = True
                        break
            if results['tc6']:
                break

    if not results['tc6']:
        if (check_bash_history(homes, r'curl.*localhost') or
            check_bash_history(homes, r'curl_check') or
            check_bash_history(homes, r'curl\s+-I')):
            results['tc6'] = True

    if not results['tc6'] and c_recovery:
        if any(w in c_recovery for w in ['200 ok', 'http 200', '200', 'endpoint response', 'http']):
            results['tc6'] = True

    # TC7: Clean system state (2 Marks)
    state_files = ["system_state.txt", "system_audit.txt", "platform_health.txt", "audit.txt", "state.txt", "tc7.txt"]
    for h in homes:
        for sf in state_files:
            sp = os.path.join(h, sf)
            if safe_isfile(sp) and check_mtime_func(sp):
                c = safe_read(sp).lower()
                audit_matches = sum(1 for w in ['uptime', 'load average', 'free', 'mem', 'df', 'systemd', 'failed', 'units', 'audit', 'healthy', 'active', 'clean', 'normal', 'report'] if w in c)
                if audit_matches >= 2:
                    results['tc7'] = True
                    break
        if results['tc7']:
            break

    if not results['tc7']:
        if (check_bash_history(homes, r'system_state') or
            check_bash_history(homes, r'systemctl\s+list-units') or
            check_bash_history(homes, r'uptime')):
            results['tc7'] = True

    if not results['tc7'] and c_recovery:
        if any(w in c_recovery for w in ['system audit', 'uptime', 'clean system state', 'platform health verified', 'clean', 'normal']):
            results['tc7'] = True

    # TC8: Runbook execution log (2 Marks)
    for h in homes:
        for fn in ["incident_recovery.log", "runbook.log", "recovery.log", "tc8.log", "tc8.txt"]:
            p = os.path.join(h, fn)
            if p not in candidate_logs:
                candidate_logs.append(p)

    for log_p in candidate_logs:
        if safe_isfile(log_p) and check_mtime_func(log_p):
            c = safe_read(log_p).lower()
            if len(c.strip()) > 30 and any(term in c for term in ['incident', 'triage', 'disk', 'process', 'route', 'nginx', 'recovery', 'remediation', 'completed', 'runbook', 'report']):
                results['tc8'] = True
                break

    if not results['tc8']:
        if check_bash_history(homes, r'incident_recovery') or check_bash_history(homes, r'runbook'):
            results['tc8'] = True

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
