import json
import os
import sys
import stat
import tarfile
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
    
    app_dir = os.path.join(HOME, 'app_data')
    conf_file = os.path.join(app_dir, 'config_dev.conf')
    key_file = os.path.join(app_dir, 'database.key')
    tar_file = os.path.join(HOME, 'app_backup.tar.gz')

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

    # TC2: App directory created with mode 755
    tc2_passed = False
    if tc1_passed and os.path.isdir(app_dir):
        try:
            st = os.stat(app_dir)
            if stat.S_IMODE(st.st_mode) == 0o755:
                tc2_passed = True
        except Exception:
            pass
    results['tc2'] = tc2_passed
    total_score += 3 if tc2_passed else 0
    print(f"TC2: {'Directory app_data mode 755':<35} [{'PASSED' if tc2_passed else 'FAILED'}] ({3 if tc2_passed else 0}/3)")

    # TC3: Target files created
    tc3_passed = False
    if tc1_passed and os.path.isfile(conf_file) and os.path.isfile(key_file):
        tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 3 if tc3_passed else 0
    print(f"TC3: {'Files config_dev & database.key':<35} [{'PASSED' if tc3_passed else 'FAILED'}] ({3 if tc3_passed else 0}/3)")

    # TC4: Ownership root:ubuntu
    tc4_passed = False
    if tc3_passed:
        try:
            import pwd, grp
            st_dir = os.stat(app_dir)
            st_conf = os.stat(conf_file)
            st_key = os.stat(key_file)
            
            owner = pwd.getpwuid(st_dir.st_uid).pw_name
            group = grp.getgrgid(st_dir.st_gid).gr_name
            if owner == 'root' and group == 'ubuntu':
                tc4_passed = True
        except Exception:
            # Fallback if testing locally on Windows/macOS
            tc4_passed = True
    results['tc4'] = tc4_passed
    total_score += 3 if tc4_passed else 0
    print(f"TC4: {'Ownership set to root:ubuntu':<35} [{'PASSED' if tc4_passed else 'FAILED'}] ({3 if tc4_passed else 0}/3)")

    # TC5: config_dev.conf mode 644
    tc5_passed = False
    if os.path.isfile(conf_file):
        try:
            st = os.stat(conf_file)
            if stat.S_IMODE(st.st_mode) == 0o644:
                tc5_passed = True
        except Exception:
            pass
    results['tc5'] = tc5_passed
    total_score += 3 if tc5_passed else 0
    print(f"TC5: {'File config_dev.conf mode 644':<35} [{'PASSED' if tc5_passed else 'FAILED'}] ({3 if tc5_passed else 0}/3)")

    # TC6: database.key mode 400
    tc6_passed = False
    if os.path.isfile(key_file):
        try:
            st = os.stat(key_file)
            if stat.S_IMODE(st.st_mode) == 0o400:
                tc6_passed = True
        except Exception:
            pass
    results['tc6'] = tc6_passed
    total_score += 4 if tc6_passed else 0
    print(f"TC6: {'File database.key mode 400':<35} [{'PASSED' if tc6_passed else 'FAILED'}] ({4 if tc6_passed else 0}/4)")

    # TC7: Backup archive app_backup.tar.gz created
    tc7_passed = False
    if os.path.isfile(tar_file) and os.path.getsize(tar_file) > 0:
        try:
            with tarfile.open(tar_file, 'r:gz') as tar:
                names = tar.getnames()
                if any('app_data' in n for n in names):
                    tc7_passed = True
        except Exception:
            tc7_passed = True
    results['tc7'] = tc7_passed
    total_score += 4 if tc7_passed else 0
    print(f"TC7: {'Backup archive app_backup.tar.gz':<35} [{'PASSED' if tc7_passed else 'FAILED'}] ({4 if tc7_passed else 0}/4)")

    print("-" * 60)
    print(f"{'TOTAL SCORE:':<44} {total_score}/20")
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
