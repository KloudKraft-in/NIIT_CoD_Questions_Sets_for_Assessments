import json
import os
import sys
from datetime import datetime, timezone, timedelta
import socket

def get_home():
    if os.path.isdir('/home/ubuntu') and (os.path.exists('/home/ubuntu/workspace') or os.path.exists('/home/ubuntu/final.txt')):
        return '/home/ubuntu'
    if os.path.isdir('/home/Niit') and (os.path.exists('/home/Niit/workspace') or os.path.exists('/home/Niit/final.txt')):
        return '/home/Niit'
    return os.path.expanduser('~')

HOME = get_home()

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', 'LOCAL_USER')

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
    print(f"{'NIIT LOCAL LINUX DIRECTORY OPERATIONS VERIFICATION':^60}")
    print("-" * 60)

    total_score = 0
    results = {}

    def check_mtime(path):
        if not START_TIME:
            return True
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
            return mtime >= START_TIME - timedelta(minutes=5)
        except Exception:
            return False

    # TC1: Environment active and verified
    tc1_passed = os.path.exists(HOME) and os.path.isdir(HOME)
    results['tc1'] = tc1_passed
    total_score += 0
    print(f"TC1: {'Local VM Environment active':<30} [{'PASSED' if tc1_passed else 'FAILED'}] (0/0)")

    # TC2: Directory 'workspace' and file 'temp.txt' created successfully
    tc2_passed = False
    if tc1_passed:
        target_dir = os.path.join(HOME, 'workspace')
        target_file = os.path.join(target_dir, 'temp.txt')
        final_file = os.path.join(HOME, 'final.txt')
        if os.path.isdir(target_dir) and (os.path.isfile(target_file) or os.path.isfile(final_file)):
            if check_mtime(target_dir) or check_mtime(target_file) or check_mtime(final_file):
                tc2_passed = True
    results['tc2'] = tc2_passed
    total_score += 5 if tc2_passed else 0
    print(f"TC2: {'workspace/temp.txt created':<30} [{'PASSED' if tc2_passed else 'FAILED'}] ({5 if tc2_passed else 0}/5)")

    # TC3: File moved and renamed to '/home/ubuntu/final.txt' successfully
    tc3_passed = False
    if tc1_passed:
        final_file = os.path.join(HOME, 'final.txt')
        if os.path.isfile(final_file):
            if check_mtime(final_file):
                tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 5 if tc3_passed else 0
    print(f"TC3: {'temp.txt moved and renamed to final.txt':<30} [{'PASSED' if tc3_passed else 'FAILED'}] ({5 if tc3_passed else 0}/5)")

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
    with open(os.path.join(ws_path, 'solution.py'), 'w') as f:
        json.dump(output_data, f, indent=4)
        
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
        json.dump(output_data, f, indent=4)
    with open(os.path.join(root_ws_path, 'solution.py'), 'w') as f:
        json.dump(output_data, f, indent=4)

if __name__ == "__main__":
    verify_task()
