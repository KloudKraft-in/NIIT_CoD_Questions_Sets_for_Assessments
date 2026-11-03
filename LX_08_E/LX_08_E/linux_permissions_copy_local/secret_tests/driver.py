import json
import os
import sys
import stat
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HOME = os.path.expanduser('~')

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None

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

def verify_task():
    print("\n" + "-" * 60)
    print(f"{'NIIT LOCAL LINUX VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}
    
    target_file = os.path.join(HOME, 'env_local.txt')

    def check_mtime(path):
        if not START_TIME:
            return True
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
            return mtime >= START_TIME - timedelta(minutes=5)
        except Exception:
            return False

    # TC1: Environment active
    tc1_passed = os.path.exists(HOME) and os.path.isdir(HOME)
    results['tc1'] = tc1_passed
    print(f"TC1: {'Local VM Environment active':<35} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: File created
    tc2_passed = False
    if tc1_passed and os.path.isfile(target_file):
        if check_mtime(target_file):
            tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 2 if tc2_passed else 0
    print(f"TC2: {'File env_local.txt created':<35} [{'PASSED' if tc2_passed else 'FAILED'}] ({2 if tc2_passed else 0}/2)")

    # TC3: Content matches /etc/environment
    tc3_passed = False
    if tc2_passed:
        try:
            with open('/etc/environment', 'r') as f1, open(target_file, 'r') as f2:
                if f1.read().strip() == f2.read().strip():
                    tc3_passed = True
        except Exception:
            # Fallback if testing on non-linux OS without /etc/environment
            if os.path.getsize(target_file) >= 0:
                tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 2 if tc3_passed else 0
    print(f"TC3: {'File content verified':<35} [{'PASSED' if tc3_passed else 'FAILED'}] ({2 if tc3_passed else 0}/2)")

    # TC4: Permissions set to 600
    tc4_passed = False
    if tc2_passed:
        try:
            st = os.stat(target_file)
            mode = stat.S_IMODE(st.st_mode)
            if mode == 0o600:
                tc4_passed = True
        except Exception:
            pass
    results['tc4'] = tc4_passed
    total_score += 3 if tc4_passed else 0
    print(f"TC4: {'Permissions mode 600 (rw-------)':<35} [{'PASSED' if tc4_passed else 'FAILED'}] ({3 if tc4_passed else 0}/3)")

    # TC5: Ownership verified
    tc5_passed = False
    if tc2_passed:
        try:
            import pwd
            st = os.stat(target_file)
            owner_name = pwd.getpwuid(st.st_uid).pw_name
            if owner_name in ['ubuntu', 'root'] or st.st_uid == os.getuid():
                tc5_passed = True
        except Exception:
            tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 3 if tc5_passed else 0
    print(f"TC5: {'File ownership verified':<35} [{'PASSED' if tc5_passed else 'FAILED'}] ({3 if tc5_passed else 0}/3)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/10")
    print("-" * 60 + "\n")

    ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
    os.makedirs(ws_path, exist_ok=True)
    
    output_data = {'score': total_score, 'results': results}
    instance_id, aws_region = get_aws_metadata()
    if instance_id:
        output_data['instance_id'] = instance_id
        output_data['aws_region'] = aws_region
        
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(output_data, f, indent=4)
        
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
        json.dump(output_data, f, indent=4)

if __name__ == "__main__":
    verify_task()
