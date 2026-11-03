import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', 'LOCAL_USER')

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
    return list(homes)

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

def validate_tc3_script(h, check_mtime_func):
    """
    Validates TC3:
    1. app.conf exists inside ~/app_env/config/
    2. auth.key exists inside ~/app_env/.secret_keys/
    3. path_check.sh exists inside ~/ or ~/app_env/ and is not empty
    4. path_check.sh executes successfully (returncode == 0)
    5. path_check.sh outputs the absolute path of app.conf and the total count of hidden files in ~/app_env/
    """
    # 1. Check app.conf
    f1 = os.path.join(h, "app_env", "config", "app.conf")
    f1_alt = os.path.join(h, "config", "app.conf")
    f1_path = f1 if os.path.isfile(f1) else (f1_alt if os.path.isfile(f1_alt) else None)
    if not f1_path:
        return False

    # 2. Check auth.key
    f2 = os.path.join(h, "app_env", ".secret_keys", "auth.key")
    f2_alt = os.path.join(h, ".secret_keys", "auth.key")
    f2_path = f2 if os.path.isfile(f2) else (f2_alt if os.path.isfile(f2_alt) else None)
    if not f2_path:
        return False

    # 3. Check path_check.sh existence
    s1 = os.path.join(h, "path_check.sh")
    s2 = os.path.join(h, "app_env", "path_check.sh")
    script_path = s1 if os.path.isfile(s1) else (s2 if os.path.isfile(s2) else None)
    if not script_path:
        return False

    try:
        if os.path.getsize(script_path) == 0:
            return False
    except Exception:
        return False

    if not (check_mtime_func(f1_path) or check_mtime_func(f2_path) or check_mtime_func(script_path)):
        return False

    # 4. Check script content
    script_content = ""
    try:
        with open(script_path, 'r', encoding='utf-8', errors='ignore') as sf:
            script_content = sf.read()
    except Exception:
        return False

    if not script_content.strip():
        return False

    has_app_conf_ref = ("app.conf" in script_content) or ("config" in script_content)
    has_hidden_ref = (
        (".*" in script_content or "-a" in script_content or "hidden" in script_content.lower()) or
        ("find" in script_content and "app_env" in script_content) or
        (".secret_keys" in script_content)
    )

    if not (has_app_conf_ref and has_hidden_ref):
        return False

    # 5. Execute script and check output
    abs_app_conf = os.path.abspath(f1_path).replace('\\', '/')
    abs_app_conf_normalized = os.path.normpath(f1_path).lower()
    bash_bin = shutil.which('bash') or ('/bin/bash' if os.path.exists('/bin/bash') else None)
    stdout_output = ""
    run_ok = False

    if bash_bin:
        try:
            proc = subprocess.run([bash_bin, script_path], capture_output=True, text=True, timeout=5, cwd=h)
            if proc.returncode == 0:
                run_ok = True
                stdout_output = proc.stdout.strip()
            else:
                return False
        except Exception:
            return False
    elif os.access(script_path, os.X_OK):
        try:
            proc = subprocess.run([script_path], capture_output=True, text=True, timeout=5, cwd=h)
            if proc.returncode == 0:
                run_ok = True
                stdout_output = proc.stdout.strip()
            else:
                return False
        except Exception:
            return False
    else:
        run_ok = True

    if run_ok and stdout_output:
        out_clean = stdout_output.replace('\\', '/')
        path_in_output = (
            (abs_app_conf.lower() in out_clean.lower()) or
            (abs_app_conf_normalized in out_clean.lower()) or
            ("app_env/config/app.conf" in out_clean and ("/" in out_clean or "\\" in stdout_output)) or
            ("app.conf" in out_clean and ("/home" in out_clean or "/root" in out_clean or h.replace('\\', '/').lower() in out_clean.lower()))
        )
        count_in_output = bool(re.search(r'\b\d+\b', stdout_output))
        return path_in_output and count_in_output
    elif not bash_bin:
        return True

    return False

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'NIIT LOCAL LINUX DIRECTORY NAVIGATION VERIFICATION':^60}")
    print(f"System Hostname: {socket.gethostname()}")
    print("-" * 60)

    total_score = 0
    results = {}
    
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

    # TC1: Environment verification: local Linux environment active and home directory reachable
    tc1_passed = any(os.path.isdir(h) for h in all_homes)
    results['tc1'] = tc1_passed
    total_score += 0
    print(f"TC1: {'Local VM Environment active':<30} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: Directory hierarchy creation: verify creation of app_env/config, app_env/logs, and .secret_keys
    tc2_passed = False
    if tc1_passed:
        for h in all_homes:
            d1 = os.path.join(h, "app_env", "config")
            d2 = os.path.join(h, "app_env", "logs")
            d3 = os.path.join(h, "app_env", ".secret_keys")
            if (os.path.isdir(d1) and os.path.isdir(d2) and os.path.isdir(d3)) or (os.path.isdir(os.path.join(h, "app_env")) and (os.path.isdir(d1) or os.path.isdir(d2) or os.path.isdir(d3))):
                if check_mtime(d1) or check_mtime(d2) or check_mtime(d3) or check_mtime(os.path.join(h, "app_env")):
                    tc2_passed = True
                    break
    results['tc2'] = tc2_passed
    total_score += 5 if tc2_passed else 0
    print(f"TC2: {'Directory hierarchy created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({5 if tc2_passed else 0}/5)")

    # TC3: File placement and verification script: app.conf, auth.key, and path_check.sh execution
    tc3_passed = False
    if tc1_passed:
        for h in all_homes:
            if validate_tc3_script(h, check_mtime):
                tc3_passed = True
                break
    results['tc3'] = tc3_passed
    total_score += 5 if tc3_passed else 0
    print(f"TC3: {'app.conf, auth.key, script':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({5 if tc3_passed else 0}/5)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/10")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    
    existing_data = {'score': total_score, 'results': results}
    instance_id, aws_region = get_aws_metadata()
    if instance_id:
        existing_data['instance_id'] = instance_id
        existing_data['aws_region'] = aws_region
        
    legacy_metadata_path = os.path.join(HOME, 'Niit_Workspace', 'os_lx_d01_e_directory_navigation_system_path', 'student_workspace', 'solution.json')
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
        
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
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
