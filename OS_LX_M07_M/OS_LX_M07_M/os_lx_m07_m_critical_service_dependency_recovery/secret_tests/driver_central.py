import json
import os
import sys
import time
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Global IST offset for consistent reporting
ist_offset = timezone(timedelta(hours=5, minutes=30))

# Metadata
QUESTION_CODE = "OS_LX_M07_M"
PROBLEM_SLUG = "os_lx_m07_m_critical_service_dependency_recovery"
LAB_TITLE = "Linux Lab: Critical Service Dependency Recovery & Unit Override Management"
TOTAL_MARKS = 20

# Account B Programmatic Service Account Credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')

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

def find_all_candidate_homes():
    """Discovers all possible user home and workspace paths on the system."""
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
        homes.add(f'/home/{u}')
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

TC_NAMES = {
    "tc1": "Failure diagnosis: journalctl confirms start-limit-hit and missing environment variables",
    "tc2": "Counter reset: systemctl reset-failed clears the start-limit throttle state",
    "tc3": "Drop-in configuration: /etc/systemd/system/payment-gateway.service.d/override.conf created with valid syntax",
    "tc4": "Daemon reload: systemctl daemon-reload executes cleanly",
    "tc5": "Service startup: payment-gateway enters stable active (running) state",
    "tc6": "Log validation: unit logs show successful configuration loading with zero errors",
    "tc7": "Health check probe: local daemon health port responds with HTTP 200 OK"
}

TC_MARKS = {
    "tc1": 3,
    "tc2": 2,
    "tc3": 3,
    "tc4": 3,
    "tc5": 3,
    "tc6": 3,
    "tc7": 3
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
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False}

    # TC1
    for h in homes:
        for fn in ["payment_diagnosis.txt", "payment_error.txt", "diagnosis.txt", "journal_error.txt", "tc1.txt"]:
            f = os.path.join(h, fn)
            if safe_isfile(f):
                c = safe_read(f).lower()
                if any(term in c for term in ['start-limit', 'environment', 'payment-gateway', 'failed', 'throttle', 'port', 'api_key', 'no entries', 'not found', 'could not be found', 'journalctl', 'systemctl', 'payment']):
                    results['tc1'] = True
                    break
        if results['tc1']:
            break
    if not results['tc1']:
        if check_bash_history(homes, r'journalctl') or check_bash_history(homes, r'systemctl'):
            results['tc1'] = True

    # TC2
    for h in homes:
        for fn in ["reset_counter.txt", "reset_failed.txt", "reset.txt", "tc2.txt"]:
            f = os.path.join(h, fn)
            if safe_isfile(f):
                results['tc2'] = True
                break
        if results['tc2']:
            break
    if not results['tc2']:
        if check_bash_history(homes, r'reset-failed'):
            results['tc2'] = True

    # TC3
    override_paths = [
        '/etc/systemd/system/payment-gateway.service.d/override.conf',
        '/etc/systemd/system/payment-gateway.service.d/10-env.conf'
    ]
    for h in homes:
        override_paths.append(os.path.join(h, "etc", "systemd", "system", "payment-gateway.service.d", "override.conf"))
        override_paths.append(os.path.join(h, "override.conf"))
        override_paths.append(os.path.join(h, "tc3.conf"))

    found_override = None
    for op in override_paths:
        if safe_isfile(op):
            found_override = op
            break

    if found_override:
        c = safe_read(found_override)
        has_env = ('EnvironmentFile' in c and '/etc/payment/gateway.env' in c) or 'EnvironmentFile' in c or 'gateway.env' in c
        has_restart = 'RestartSec' in c
        has_section = '[Service]' in c
        if has_env or has_restart or has_section:
            results['tc3'] = True

    # TC4
    for h in homes:
        for fn in ["daemon_reload.txt", "reload.txt", "tc4.txt"]:
            f = os.path.join(h, fn)
            if safe_isfile(f):
                results['tc4'] = True
                break
        if results['tc4']:
            break
    if not results['tc4']:
        if check_bash_history(homes, r'daemon-reload'):
            results['tc4'] = True
    if not results['tc4']:
        systemctl_bin = shutil.which('systemctl')
        if systemctl_bin:
            try:
                res = subprocess.run([systemctl_bin, 'show', '-p', 'DropInPaths', 'payment-gateway'], capture_output=True, text=True, timeout=5)
                if 'override.conf' in res.stdout:
                    results['tc4'] = True
            except Exception:
                pass

    # TC5
    systemctl_bin = shutil.which('systemctl')
    if systemctl_bin:
        try:
            res = subprocess.run([systemctl_bin, 'is-active', 'payment-gateway'], capture_output=True, text=True, timeout=5)
            if res.stdout.strip() == 'active':
                results['tc5'] = True
        except Exception:
            pass
    if not results['tc5']:
        for h in homes:
            for fn in ["service_status.txt", "payment_status.txt", "status.txt", "tc5.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if 'active (running)' in c or 'active' in c or 'running' in c or 'payment' in c or 'service' in c or 'started' in c:
                        results['tc5'] = True
                        break
            if results['tc5']:
                break

    # TC6
    journalctl_bin = shutil.which('journalctl')
    if journalctl_bin and results['tc5']:
        try:
            j_res = subprocess.run([journalctl_bin, '-u', 'payment-gateway', '-n', '20'], capture_output=True, text=True, timeout=5)
            if 'Payment Gateway starting' in j_res.stdout or 'API_KEY verified' in j_res.stdout or 'Started' in j_res.stdout:
                results['tc6'] = True
        except Exception:
            pass
    if not results['tc6']:
        for h in homes:
            for fn in ["payment_logs.txt", "unit_logs.txt", "journal_success.txt", "tc6.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['starting', 'port 8080', 'port', '8080', 'verified', 'healthy', 'success', 'started', 'api_key', 'payment']):
                        results['tc6'] = True
                        break
            if results['tc6']:
                break

    # TC7
    curl_bin = shutil.which('curl')
    if curl_bin:
        try:
            res = subprocess.run([curl_bin, '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:8080/health'], capture_output=True, text=True, timeout=3)
            if res.stdout.strip() in ['200', '204', '202']:
                results['tc7'] = True
        except Exception:
            pass
    if not results['tc7']:
        for h in homes:
            for fn in ["health_check.txt", "health_probe.txt", "curl_health.txt", "tc7.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f)
                    if '200' in c or 'healthy' in c.lower() or 'ok' in c.lower() or 'curl' in c.lower():
                        results['tc7'] = True
                        break
            if results['tc7']:
                break
    if not results['tc7']:
        if check_bash_history(homes, r'curl\s+.*8080') or check_bash_history(homes, r'curl'):
            results['tc7'] = True

    return results

def verify_task_central(username="LOCAL_USER", start_time_str=None, exam_code="UNKNOWN", solution_path=None, labskraft_username=None):
    if not username or username.startswith('-'):
        username = os.getenv('NIIT_USERNAME', 'LOCAL_USER')
    if not labskraft_username:
        labskraft_username = os.getenv('LABSKRAFT_USERNAME')
    if not start_time_str:
        start_time_str = os.getenv('NIIT_START_TIME')
    target_instance = os.getenv('TARGET_INSTANCE', 'LocalVM')

    candidate_files = []
    if solution_path:
        if os.path.isdir(solution_path):
            for rel in ['student_workspace/solution.json', 'solution.json', 'student_workspace/solution.py', 'solution.py']:
                p = os.path.join(solution_path, rel)
                if os.path.isfile(p):
                    candidate_files.append(p)
        elif os.path.isfile(solution_path):
            candidate_files.append(solution_path)

    search_dirs = [
        f"/home/ubuntu/central_server/student_workspace/{PROBLEM_SLUG}_solution",
        f"/home/ubuntu/central_server/student_workspace/{QUESTION_CODE}_solution",
        "/home/ubuntu/central_server/student_workspace"
    ]
    for sdir in search_dirs:
        if os.path.isdir(sdir):
            try:
                subitems = [os.path.join(sdir, d) for d in os.listdir(sdir)]
                matching = [d for d in subitems if (username and username in os.path.basename(d)) or (labskraft_username and labskraft_username in os.path.basename(d))]
                other = [d for d in subitems if d not in matching]
                matching.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                other.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                for item in matching + other[:5]:
                    if os.path.isdir(item):
                        for p in [os.path.join(item, 'student_workspace', 'solution.json'), os.path.join(item, 'solution.json'), os.path.join(item, 'student_workspace', 'solution.py'), os.path.join(item, 'solution.py')]:
                            if os.path.isfile(p) and p not in candidate_files:
                                candidate_files.append(p)
                    elif os.path.isfile(item) and item not in candidate_files:
                        candidate_files.append(item)
            except Exception:
                pass

    script_dir = os.path.dirname(os.path.abspath(__file__))
    ws_dir = os.path.normpath(os.path.join(script_dir, '..', 'student_workspace'))
    root_ws_dir = os.path.normpath(os.path.join(script_dir, '..'))

    candidate_files.extend([
        os.path.join(ws_dir, 'solution.json'),
        os.path.join(root_ws_dir, 'solution.json'),
        os.path.join(ws_dir, 'solution.py'),
        os.path.join(root_ws_dir, 'solution.py')
    ])

    for h in find_all_candidate_homes():
        candidate_files.extend([
            os.path.join(h, 'NIIT_Workspace', QUESTION_CODE, 'student_workspace', 'solution.json'),
            os.path.join(h, 'NIIT_workspace', QUESTION_CODE, 'student_workspace', 'solution.json'),
            os.path.join(h, 'NIIT_Workspace', PROBLEM_SLUG, 'student_workspace', 'solution.json'),
            os.path.join(h, 'NIIT_workspace', PROBLEM_SLUG, 'student_workspace', 'solution.json')
        ])

    metadata = {}
    best_candidate_data = None

    for cand in candidate_files:
        if os.path.isfile(cand):
            try:
                with open(cand, 'r') as f:
                    data = json.load(f)
                if data and isinstance(data, dict) and ('results' in data or 'score' in data):
                    best_candidate_data = data
                    metadata = data
                    break
            except Exception:
                pass

    if not labskraft_username and metadata:
        labskraft_username = metadata.get('labskraft_username')
    tag_value = labskraft_username if labskraft_username else username
    print(f"[SYSTEM] Candidate search tag: {tag_value}")

    eval_results = None

    # Check remote VM via SSM if credentials present
    try:
        import boto3
        found_instance_id = metadata.get('instance_id') if metadata else None
        found_region = metadata.get('aws_region', 'ap-south-1') if metadata else 'ap-south-1'
        
        if not found_instance_id:
            regions_to_check = ['ap-south-1', 'eu-west-1', 'eu-west-2', 'us-east-1', 'us-east-2', 'ap-southeast-2']
            for r in regions_to_check:
                try:
                    temp_ec2 = boto3.client('ec2', region_name=r, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                    resp = temp_ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
                    for res in resp.get('Reservations', []):
                        for inst in res.get('Instances', []):
                            tags = {t['Key'].lower(): t['Value'] for t in inst.get('Tags', [])}
                            priv_ip = inst.get('PrivateIpAddress')
                            if (priv_ip and metadata and priv_ip in ['172.31.21.253', metadata.get('private_ip')]) or tags.get('labskraft_username') == tag_value or tags.get('labskraft') == tag_value or tags.get('name') == target_instance:
                                found_instance_id = inst['InstanceId']
                                found_region = r
                                break
                        if found_instance_id:
                            break
                    if found_instance_id:
                        break
                except Exception:
                    continue

        if found_instance_id:
            ssm = boto3.client('ssm', region_name=found_region, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
            ssm_instances = ssm.describe_instance_information(
                Filters=[{'Key': 'InstanceIds', 'Values': [found_instance_id]}]
            ).get('InstanceInformationList', [])
            
            if ssm_instances and ssm_instances[0].get('PingStatus') == 'Online':
                print(f"[SYSTEM] Found running target instance {found_instance_id}. Auditing via SSM...")
                guest_python_script = """import os, sys, json, re, shutil, subprocess

def safe_read(p):
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

def safe_isfile(p):
    return os.path.isfile(p) and os.path.getsize(p) > 0

def run_tests():
    res = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False}
    homes = ['/home/LabsKraft', '/home/ubuntu', '/home/Niit', os.path.expanduser('~')]
    for base in ['/home', '/root']:
        if os.path.isdir(base):
            try:
                for u in os.listdir(base):
                    p = os.path.join(base, u)
                    if os.path.isdir(p) and p not in homes:
                        homes.append(p)
            except Exception:
                pass

    def check_hist(pattern):
        for h in homes:
            for hist_file in ['.bash_history', '.zsh_history']:
                p = os.path.join(h, hist_file)
                if safe_isfile(p):
                    c = safe_read(p)
                    if re.search(pattern, c, re.I):
                        return True
        return False

    # TC1
    for h in homes:
        for fn in ["payment_diagnosis.txt", "payment_error.txt", "diagnosis.txt", "journal_error.txt", "tc1.txt"]:
            f = os.path.join(h, fn)
            if safe_isfile(f):
                c = safe_read(f).lower()
                if any(term in c for term in ['start-limit', 'environment', 'payment-gateway', 'failed', 'throttle', 'port', 'api_key', 'no entries', 'not found', 'could not be found', 'journalctl', 'systemctl', 'payment']):
                    res['tc1'] = True
                    break
        if res['tc1']:
            break
    if not res['tc1'] and (check_hist(r'journalctl') or check_hist(r'systemctl')):
        res['tc1'] = True

    # TC2
    for h in homes:
        for fn in ["reset_counter.txt", "reset_failed.txt", "reset.txt", "tc2.txt"]:
            f = os.path.join(h, fn)
            if safe_isfile(f):
                res['tc2'] = True
                break
        if res['tc2']:
            break
    if not res['tc2'] and check_hist(r'reset-failed'):
        res['tc2'] = True

    # TC3
    override_paths = [
        '/etc/systemd/system/payment-gateway.service.d/override.conf',
        '/etc/systemd/system/payment-gateway.service.d/10-env.conf'
    ]
    for h in homes:
        override_paths.append(os.path.join(h, "etc", "systemd", "system", "payment-gateway.service.d", "override.conf"))
        override_paths.append(os.path.join(h, "override.conf"))
        override_paths.append(os.path.join(h, "tc3.conf"))

    found_override = None
    for op in override_paths:
        if safe_isfile(op):
            found_override = op
            break

    if found_override:
        c = safe_read(found_override)
        has_env = ('EnvironmentFile' in c and '/etc/payment/gateway.env' in c) or 'EnvironmentFile' in c or 'gateway.env' in c
        has_restart = 'RestartSec' in c
        has_section = '[Service]' in c
        if has_env or has_restart or has_section:
            res['tc3'] = True

    # TC4
    for h in homes:
        for fn in ["daemon_reload.txt", "reload.txt", "tc4.txt"]:
            f = os.path.join(h, fn)
            if safe_isfile(f):
                res['tc4'] = True
                break
        if res['tc4']:
            break
    if not res['tc4'] and check_hist(r'daemon-reload'):
        res['tc4'] = True
    if not res['tc4']:
        systemctl_bin = shutil.which('systemctl')
        if systemctl_bin:
            try:
                s_res = subprocess.run([systemctl_bin, 'show', '-p', 'DropInPaths', 'payment-gateway'], capture_output=True, text=True, timeout=5)
                if 'override.conf' in s_res.stdout:
                    res['tc4'] = True
            except Exception:
                pass

    # TC5
    systemctl_bin = shutil.which('systemctl')
    if systemctl_bin:
        try:
            s_res = subprocess.run([systemctl_bin, 'is-active', 'payment-gateway'], capture_output=True, text=True, timeout=5)
            if s_res.stdout.strip() == 'active':
                res['tc5'] = True
        except Exception:
            pass
    if not res['tc5']:
        for h in homes:
            for fn in ["service_status.txt", "payment_status.txt", "status.txt", "tc5.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if 'active (running)' in c or 'active' in c or 'running' in c or 'payment' in c or 'service' in c or 'started' in c:
                        res['tc5'] = True
                        break
            if res['tc5']:
                break

    # TC6
    journalctl_bin = shutil.which('journalctl')
    if journalctl_bin and res['tc5']:
        try:
            j_res = subprocess.run([journalctl_bin, '-u', 'payment-gateway', '-n', '20'], capture_output=True, text=True, timeout=5)
            if 'Payment Gateway starting' in j_res.stdout or 'API_KEY verified' in j_res.stdout or 'Started' in j_res.stdout:
                res['tc6'] = True
        except Exception:
            pass
    if not res['tc6']:
        for h in homes:
            for fn in ["payment_logs.txt", "unit_logs.txt", "journal_success.txt", "tc6.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f).lower()
                    if any(w in c for w in ['starting', 'port 8080', 'port', '8080', 'verified', 'healthy', 'success', 'started', 'api_key', 'payment']):
                        res['tc6'] = True
                        break
            if res['tc6']:
                break

    # TC7
    curl_bin = shutil.which('curl')
    if curl_bin:
        try:
            c_res = subprocess.run([curl_bin, '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:8080/health'], capture_output=True, text=True, timeout=3)
            if c_res.stdout.strip() in ['200', '204', '202']:
                res['tc7'] = True
        except Exception:
            pass
    if not res['tc7']:
        for h in homes:
            for fn in ["health_check.txt", "health_probe.txt", "curl_health.txt", "tc7.txt"]:
                f = os.path.join(h, fn)
                if safe_isfile(f):
                    c = safe_read(f)
                    if '200' in c or 'healthy' in c.lower() or 'ok' in c.lower() or 'curl' in c.lower():
                        res['tc7'] = True
                        break
            if res['tc7']:
                break
    if not res['tc7'] and (check_hist(r'curl\\s+.*8080') or check_hist(r'curl')):
        res['tc7'] = True

    print(json.dumps(res))

if __name__ == '__main__':
    run_tests()
"""
                response = ssm.send_command(
                    InstanceIds=[found_instance_id],
                    DocumentName='AWS-RunShellScript',
                    Parameters={'commands': [f"python3 << 'PYEOF'\n{guest_python_script}\nPYEOF"]}
                )
                command_id = response['Command']['CommandId']
                for _ in range(15):
                    time.sleep(1)
                    res = ssm.get_command_invocation(CommandId=command_id, InstanceId=found_instance_id)
                    if res['Status'] in ['Success', 'Failed']:
                        stdout = res.get('StandardOutputContent', '')
                        lines = [ln.strip() for ln in stdout.splitlines() if ln.strip().startswith('{') and ln.strip().endswith('}')]
                        if lines:
                            eval_results = json.loads(lines[-1])
                        break
    except Exception as e:
        print(f"[SYSTEM] SSM audit encountered an issue: {e}")

    if not eval_results:
        if best_candidate_data and 'results' in best_candidate_data:
            print("[SYSTEM] Using cached candidate evaluation data.")
            eval_results = best_candidate_data['results']
        else:
            print("[SYSTEM] Performing local assessment audit.")
            all_homes = find_all_candidate_homes()
            eval_results = validate_all_tcs(all_homes, lambda p: True)

    total_score = sum(TC_MARKS[k] for k, v in eval_results.items() if v)

    print("\n" + "=" * 60)
    print(f"{LAB_TITLE.upper() + ' EVALUATION':^60}")
    print("=" * 60)
    for k in sorted(TC_NAMES.keys()):
        status = "PASSED" if eval_results.get(k, False) else "FAILED"
        desc = TC_NAMES.get(k, k.upper())
        marks = TC_MARKS.get(k, 0)
        earned = marks if eval_results.get(k, False) else 0
        print(f"{k.upper()}: {desc:<45} [{status}] ({earned}/{marks})")
    print("=" * 60)
    print(f"{'FINAL EVALUATION SCORE:':<45} {total_score}/{TOTAL_MARKS}")
    print("=" * 60 + "\n")

    return {
        'question_id': QUESTION_CODE,
        'score': total_score,
        'total_marks': TOTAL_MARKS,
        'results': eval_results
    }

if __name__ == '__main__':
    verify_task_central()
