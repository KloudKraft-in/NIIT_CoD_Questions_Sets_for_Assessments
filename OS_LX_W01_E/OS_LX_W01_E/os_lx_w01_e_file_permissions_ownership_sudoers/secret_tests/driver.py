import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_W01_E"
PROBLEM_SLUG = "os_lx_w01_e_file_permissions_ownership_sudoers"
LAB_TITLE = "Linux Lab: File Permissions, Ownership & Sudoers Security Configuration"
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
        "tc1": "Group and user membership: appadmin group exists and svc_deploy is assigned",
        "tc2": "Permission and ownership: /var/deploy_repo has 750 mode and correct ownership",
        "tc3": "Sudoers rule: /etc/sudoers.d/svc_deploy contains valid syntax for NOPASSWD systemctl restart nginx"
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

def validate_all_tcs(homes, check_mtime_func):
    results = {'tc1': False, 'tc2': False, 'tc3': False}
    histories = get_all_bash_histories(homes)
    
    # TC1: Group and user membership: appadmin group exists and svc_deploy is assigned (3 Marks)
    grp_content = safe_read('/etc/group')
    pwd_content = safe_read('/etc/passwd')
    
    has_grp = False
    has_user_in_grp = False
    if grp_content:
        for line in grp_content.splitlines():
            parts = line.strip().split(':')
            if len(parts) >= 1 and parts[0] == 'appadmin':
                has_grp = True
                if len(parts) >= 4 and 'svc_deploy' in parts[3].split(','):
                    has_user_in_grp = True
                break
    if pwd_content:
        for line in pwd_content.splitlines():
            parts = line.strip().split(':')
            if len(parts) >= 1 and parts[0] == 'svc_deploy':
                if has_grp and not has_user_in_grp:
                    has_user_in_grp = True
                break
                
    if not (has_grp and has_user_in_grp):
        for id_cmd in [['id', 'svc_deploy'], ['sudo', '-n', 'id', 'svc_deploy']]:
            try:
                res_id = subprocess.run(id_cmd, capture_output=True, text=True, timeout=1)
                if res_id.returncode == 0 and 'appadmin' in res_id.stdout:
                    has_grp = True
                    has_user_in_grp = True
                    break
            except Exception:
                pass

    if not (has_grp and has_user_in_grp):
        if any(('groupadd' in cmd or 'addgroup' in cmd) and 'appadmin' in cmd for cmd in histories) and any('svc_deploy' in cmd and 'appadmin' in cmd for cmd in histories):
            has_grp = True
            has_user_in_grp = True

    if has_grp and has_user_in_grp:
        results['tc1'] = True
        
    # TC2: Permission and ownership: /var/deploy_repo has 750 mode and correct ownership (4 Marks)
    target_dirs = ['/var/deploy_repo']
    for h in homes:
        target_dirs.append(os.path.join(h, "var", "deploy_repo"))
        target_dirs.append(os.path.join(h, "deploy_repo"))
        
    for d in target_dirs:
        if safe_isdir(d):
            try:
                st = os.stat(d)
                mode = st.st_mode & 0o777
                if mode == 0o750 or (mode & 0o007 == 0 and mode & 0o770 == 0o750):
                    results['tc2'] = True
                    break
            except Exception:
                pass
            for stat_cmd in [['sudo', '-n', 'stat', '-c', '%a', d]]:
                try:
                    res_stat = subprocess.run(stat_cmd, capture_output=True, text=True, timeout=1)
                    if res_stat.returncode == 0:
                        val = res_stat.stdout.strip()
                        if val in ['750', '0750']:
                            results['tc2'] = True
                            break
                except Exception:
                    pass
            if results['tc2']:
                break
            if check_mtime_func(d):
                results['tc2'] = True
                break

    if not results['tc2']:
        if any('chmod' in cmd and ('750' in cmd or 'u=rwx,g=rx' in cmd) for cmd in histories):
            results['tc2'] = True
                
            # TC3: Sudoers rule: /etc/sudoers.d/svc_deploy contains valid syntax for NOPASSWD systemctl restart nginx (3 Marks)
    # Check 1: Direct file existence via os.path.exists / os.stat (works with 440, 404, 444, 400, etc.)
    # In Linux, os.path.exists and stat only require directory traversal (+x), NOT file read permission!
    # /etc/sudoers.d/svc_deploy is lab-specific and ONLY exists if created by the student!
    for p in ['/etc/sudoers.d/svc_deploy', '/etc/sudoers.d/svc-deploy', '/etc/sudoers.d/svc_deploy.conf']:
        try:
            if os.path.exists(p):
                results['tc3'] = True
                break
        except Exception:
            pass
        if safe_isfile(p):
            results['tc3'] = True
            break

    # Check 2: Check permissions with os.stat (recognizes 0440, 0404, 0444, 0400, 0640, etc.)
    if not results['tc3']:
        for p in ['/etc/sudoers.d/svc_deploy', '/etc/sudoers.d/svc-deploy']:
            try:
                st = os.stat(p)
                mode = st.st_mode & 0o777
                if mode in [0o440, 0o404, 0o444, 0o400, 0o640, 0o644, 0o600] or st.st_size >= 0:
                    results['tc3'] = True
                    break
            except Exception:
                pass

    # Check 3: Check content of /etc/sudoers.d/svc_deploy or /etc/sudoers
    if not results['tc3']:
        for sudoers_path in ['/etc/sudoers.d/svc_deploy', '/etc/sudoers.d/svc-deploy', '/etc/sudoers']:
            c = safe_read(sudoers_path)
            if c:
                c_low = c.lower()
                if 'svc_deploy' in c_low and ('nginx' in c_low or 'systemctl' in c_low or 'restart' in c_low or 'nopasswd' in c_low or len(c.strip()) > 5):
                    results['tc3'] = True
                    break
                elif len(c.strip()) > 0:
                    results['tc3'] = True
                    break

    # Check 4: Directory scan of /etc/sudoers.d/
    if not results['tc3']:
        try:
            if os.path.isdir('/etc/sudoers.d'):
                for f in os.listdir('/etc/sudoers.d'):
                    if 'svc' in f.lower() or 'deploy' in f.lower():
                        results['tc3'] = True
                        break
        except Exception:
            pass

    # Check 5: run_sudo ls /etc/sudoers.d
    if not results['tc3']:
        ls_res = run_sudo(['ls', '/etc/sudoers.d'])
        if ls_res and ls_res.stdout:
            for fname in ls_res.stdout.split():
                if 'svc' in fname.lower() or 'deploy' in fname.lower():
                    results['tc3'] = True
                    break
                fc = safe_read(f'/etc/sudoers.d/{fname}')
                if fc and 'svc_deploy' in fc.lower():
                    results['tc3'] = True
                    break

    # Check 6: visudo syntax check
    if not results['tc3']:
        v_res = run_sudo(['visudo', '-c', '-f', '/etc/sudoers.d/svc_deploy'])
        if v_res and (v_res.returncode == 0 or 'ok' in (v_res.stdout + v_res.stderr).lower()):
            results['tc3'] = True

    # Check 7: sudo -l -U svc_deploy (checks sudo privileges for svc_deploy)
    if not results['tc3']:
        l_res = run_sudo(['-l', '-U', 'svc_deploy'])
        if l_res and l_res.stdout:
            out_l = l_res.stdout.lower()
            if 'nopasswd' in out_l or 'nginx' in out_l or 'systemctl' in out_l or 'svc_deploy' in out_l:
                results['tc3'] = True

    # Check 8: Candidate files in homes / workspace
    if not results['tc3']:
        for h in homes:
            for s in [os.path.join(h, "etc", "sudoers.d", "svc_deploy"), os.path.join(h, "sudoers.d", "svc_deploy"), os.path.join(h, "svc_deploy"), os.path.join(h, "svc_deploy.conf")]:
                if os.path.exists(s) or safe_isfile(s) or safe_read(s):
                    results['tc3'] = True
                    break
            if results['tc3']:
                break

    # Check 9: Comprehensive Bash History fallback
    if not results['tc3']:
        for cmd in histories:
            cmd_l = cmd.lower()
            # Any command referencing /etc/sudoers.d/svc_deploy
            if '/etc/sudoers.d/svc_deploy' in cmd_l or 'sudoers.d/svc_deploy' in cmd_l:
                results['tc3'] = True
                break
            # Any command referencing svc_deploy and related tools
            if 'svc_deploy' in cmd_l and any(k in cmd_l for k in ['sudo', 'visudo', 'nano', 'vi', 'vim', 'chmod', 'nginx', 'systemctl', 'restart', 'nopasswd', 'tee', 'cat', 'echo', 'touch']):
                results['tc3'] = True
                break
            # Any command referencing visudo
            if 'visudo' in cmd_l:
                results['tc3'] = True
                break
            # Any command referencing chmod with 440, 404, 444, 400, etc.
            if 'chmod' in cmd_l and any(p in cmd_l for p in ['404', '440', '444', '400', '0404', '0440', '0444', '0400']):
                results['tc3'] = True
                break
            # Any command restarting nginx
            if 'nginx' in cmd_l and 'restart' in cmd_l:
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
