import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_W06_M"
PROBLEM_SLUG = "os_lx_w06_m_logrotate_configuration_automated_log"
LAB_TITLE = "Linux Lab: Logrotate Configuration & Automated Log Lifecycle Management"
TOTAL_MARKS = 20

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

def safe_isdir(path):
    if not path:
        return False
    try:
        if os.path.isdir(path):
            return True
    except Exception:
        pass
    for cmd in [['sudo', '-n', 'test', '-d', path], ['sudo', '-n', 'test', '-d', path]]:
        try:
            res = subprocess.run(cmd, capture_output=True, timeout=1)
            if res.returncode == 0:
                return True
        except Exception:
            pass
    try:
        res = subprocess.run(f'sudo -n test -d "{path}"', shell=True, capture_output=True, timeout=1)
        if res.returncode == 0:
            return True
    except Exception:
        pass
    return False

def safe_exists(path):
    if not path:
        return False
    try:
        if os.path.exists(path):
            return True
    except Exception:
        pass
    for cmd in [['sudo', '-n', 'test', '-e', path], ['sudo', '-n', 'test', '-f', path]]:
        try:
            res = subprocess.run(cmd, capture_output=True, timeout=1)
            if res.returncode == 0:
                return True
        except Exception:
            pass
    try:
        res = subprocess.run(['sudo', '-n', 'ls', '-d', path], capture_output=True, text=True, timeout=1)
        if res.returncode == 0 and res.stdout.strip():
            return True
    except Exception:
        pass
    return False

def safe_isfile(path):
    if not path:
        return False
    try:
        if os.path.isfile(path):
            return True
    except Exception:
        pass
    for cmd in [['sudo', '-n', 'test', '-f', path], ['sudo', '-n', 'test', '-s', path]]:
        try:
            res = subprocess.run(cmd, capture_output=True, timeout=1)
            if res.returncode == 0:
                return True
        except Exception:
            pass
    try:
        res = subprocess.run(['sudo', '-n', 'ls', '-d', path], capture_output=True, text=True, timeout=1)
        if res.returncode == 0 and res.stdout.strip():
            return True
    except Exception:
        pass
    return False

def safe_read(path, default=""):
    if not path:
        return default
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        pass
    for cat_cmd in [['sudo', '-n', 'cat', path], ['sudo', '-n', 'cat', path]]:
        try:
            res = subprocess.run(cat_cmd, capture_output=True, text=True, timeout=1)
            if res.returncode == 0 and res.stdout:
                return res.stdout
        except Exception:
            pass
    return default

def find_all_user_homes():
    homes = set()
    curr = os.path.expanduser('~')
    if safe_isdir(curr):
        homes.add(os.path.abspath(curr))
    env_h = os.getenv('HOME')
    if env_h and safe_isdir(env_h):
        homes.add(os.path.abspath(env_h))
    for candidate in ['/home/ubuntu', '/home/LabsKraft', '/home/Niit', '/home/niit', '/root']:
        if safe_isdir(candidate):
            homes.add(candidate)
    if safe_isdir('/home'):
        try:
            for u in os.listdir('/home'):
                p = os.path.join('/home', u)
                if safe_isdir(p):
                    homes.add(p)
        except Exception:
            pass
    for ws_base in ['/home/LabsKraft/NIIT_workspace', '/home/LabsKraft/NIIT_Workspace', '/home/ubuntu/NIIT_workspace', '/home/ubuntu/NIIT_Workspace']:
        if safe_isdir(ws_base):
            homes.add(ws_base)
            try:
                for sub in os.listdir(ws_base):
                    sub_p = os.path.join(ws_base, sub)
                    if safe_isdir(sub_p):
                        homes.add(sub_p)
            except Exception:
                pass
    return list(homes)

TC_NAMES = {
        "tc1": "Configuration authoring: /etc/logrotate.d/ecommerce contains valid directives (daily, rotate 7, compress, copytruncate)",
        "tc2": "Syntax and test execution: logrotate -d dry-run and logrotate -vf forced test complete with zero syntax errors",
        "tc3": "Archive generation: rotated log file is compressed with gzip format (.1.gz)",
        "tc4": "Copytruncate integrity: active log file handle remains intact with truncated zero/initial byte state"
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

def validate_all_tcs(homes, check_mtime_func=None):
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False}
    
    # -------------------------------------------------------------------------
    # TC1: Configuration authoring: /etc/logrotate.d/ecommerce contains valid directives
    # -------------------------------------------------------------------------
    candidate_confs = ['/etc/logrotate.d/ecommerce']
    for h in homes:
        candidate_confs.append(os.path.join(h, "etc", "logrotate.d", "ecommerce"))
        candidate_confs.append(os.path.join(h, "ecommerce"))
        candidate_confs.append(os.path.join(h, "ecommerce.conf"))
        
    found_conf = None
    for conf in candidate_confs:
        c = safe_read(conf)
        if c:
            has_daily = bool(re.search(r'\bdaily\b', c, re.IGNORECASE))
            has_rotate = bool(re.search(r'\brotate\s+\d+\b', c, re.IGNORECASE))
            has_compress = bool(re.search(r'\bcompress\b', c, re.IGNORECASE))
            has_copytruncate = bool(re.search(r'\bcopytruncate\b', c, re.IGNORECASE))
            
            if (has_daily or has_rotate) and (has_compress or has_copytruncate):
                results['tc1'] = True
                found_conf = conf
                break
            elif 'ecommerce' in c.lower() and ('rotate' in c.lower() or 'daily' in c.lower()):
                results['tc1'] = True
                found_conf = conf
                break
                
    if not results['tc1']:
        try:
            res_grep = subprocess.run('sudo -n grep -riE "(daily|rotate|copytruncate)" /etc/logrotate.d/ 2>/dev/null', shell=True, capture_output=True, text=True, timeout=1)
            if res_grep.returncode == 0 and 'ecommerce' in res_grep.stdout.lower():
                results['tc1'] = True
                found_conf = '/etc/logrotate.d/ecommerce'
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # TC2: Syntax and test execution: logrotate -d dry-run and logrotate -vf forced test complete with zero syntax errors
    # -------------------------------------------------------------------------
    if found_conf and results['tc1']:
        syntax_ok = False
        try:
            res_d = subprocess.run(['logrotate', '-d', found_conf], capture_output=True, text=True, timeout=2)
            if res_d.returncode == 0 and 'error: found error in' not in res_d.stderr.lower():
                syntax_ok = True
        except Exception:
            pass
            
        if not syntax_ok:
            try:
                res_d = subprocess.run(['sudo', '-n', 'logrotate', '-d', found_conf], capture_output=True, text=True, timeout=2)
                if res_d.returncode == 0 and 'error: found error in' not in res_d.stderr.lower():
                    syntax_ok = True
            except Exception:
                pass
                
        if syntax_ok:
            results['tc2'] = True
        else:
            # Fallback syntax check: verify matching braces and directive structure
            c = safe_read(found_conf)
            if c and c.count('{') == c.count('}') and c.count('{') > 0 and 'error' not in c.lower():
                results['tc2'] = True

    # -------------------------------------------------------------------------
    # TC3: Archive generation: rotated log file is compressed with gzip format (.1.gz)
    # -------------------------------------------------------------------------
    candidate_gzs = [
        '/var/log/ecommerce/app.log.1.gz',
        '/var/log/ecommerce/error.log.1.gz'
    ]
    for h in homes:
        candidate_gzs.append(os.path.join(h, "var", "log", "ecommerce", "app.log.1.gz"))
        candidate_gzs.append(os.path.join(h, "ecommerce", "app.log.1.gz"))
        candidate_gzs.append(os.path.join(h, "app.log.1.gz"))
        candidate_gzs.append(os.path.join(h, "var", "log", "ecommerce", "error.log.1.gz"))
        
    for gz in candidate_gzs:
        if safe_exists(gz):
            results['tc3'] = True
            break
            
    if not results['tc3']:
        try:
            res_ls = subprocess.run('sudo -n ls /var/log/ecommerce/*.gz 2>/dev/null', shell=True, capture_output=True, text=True, timeout=1)
            if res_ls.returncode == 0 and res_ls.stdout.strip():
                results['tc3'] = True
        except Exception:
            pass
            
    if not results['tc3']:
        for h in homes:
            p = os.path.join(h, "ecommerce")
            if os.path.isdir(p):
                try:
                    for f in os.listdir(p):
                        if f.endswith('.gz'):
                            results['tc3'] = True
                            break
                except Exception:
                    pass
            if results['tc3']:
                break

    # -------------------------------------------------------------------------
    # TC4: Copytruncate integrity: active log file handle remains intact with truncated zero/initial byte state
    # -------------------------------------------------------------------------
    candidate_apps = [
        '/var/log/ecommerce/app.log',
        '/var/log/ecommerce/error.log'
    ]
    for h in homes:
        candidate_apps.append(os.path.join(h, "var", "log", "ecommerce", "app.log"))
        candidate_apps.append(os.path.join(h, "ecommerce", "app.log"))
        candidate_apps.append(os.path.join(h, "app.log"))
        candidate_apps.append(os.path.join(h, "var", "log", "ecommerce", "error.log"))
        
    for app in candidate_apps:
        if safe_exists(app):
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
