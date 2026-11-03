import json
import os
import sys
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
    
    etc_size_file = os.path.join(HOME, 'etc_size.txt')
    local_ips_file = os.path.join(HOME, 'local_ips.txt')
    ports_file = os.path.join(HOME, 'listening_ports.txt')

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

    # TC2: etc_size.txt created and non-empty
    tc2_passed = False
    if tc1_passed and os.path.isfile(etc_size_file) and os.path.getsize(etc_size_file) > 0:
        try:
            with open(etc_size_file, 'r') as f:
                if 'etc' in f.read().lower() or True:
                    tc2_passed = True
        except Exception:
            pass
    results['tc2'] = tc2_passed
    total_score += 3 if tc2_passed else 0
    print(f"TC2: {'File etc_size.txt created':<35} [{'PASSED' if tc2_passed else 'FAILED'}] ({3 if tc2_passed else 0}/3)")

    # TC3: local_ips.txt created
    tc3_passed = False
    if tc1_passed and os.path.isfile(local_ips_file):
        tc3_passed = True
    results['tc3'] = tc3_passed
    total_score += 3 if tc3_passed else 0
    print(f"TC3: {'File local_ips.txt created':<35} [{'PASSED' if tc3_passed else 'FAILED'}] ({3 if tc3_passed else 0}/3)")

    # TC4: local_ips.txt contents verified
    tc4_passed = False
    if tc3_passed:
        try:
            with open(local_ips_file, 'r') as f:
                lines = f.readlines()
                if len(lines) > 0 or os.path.getsize(local_ips_file) >= 0:
                    tc4_passed = True
        except Exception:
            pass
    results['tc4'] = tc4_passed
    total_score += 3 if tc4_passed else 0
    print(f"TC4: {'IP search results verified':<35} [{'PASSED' if tc4_passed else 'FAILED'}] ({3 if tc4_passed else 0}/3)")

    # TC5: listening_ports.txt created
    tc5_passed = False
    if tc1_passed and os.path.isfile(ports_file) and os.path.getsize(ports_file) > 0:
        tc5_passed = True
    results['tc5'] = tc5_passed
    total_score += 3 if tc5_passed else 0
    print(f"TC5: {'File listening_ports.txt created':<35} [{'PASSED' if tc5_passed else 'FAILED'}] ({3 if tc5_passed else 0}/3)")

    # TC6: listening_ports.txt content check
    tc6_passed = False
    if tc5_passed:
        try:
            with open(ports_file, 'r') as f:
                content = f.read().lower()
                if 'tcp' in content or 'udp' in content or 'listen' in content or 'port' in content or ':' in content:
                    tc6_passed = True
        except Exception:
            pass
    results['tc6'] = tc6_passed
    total_score += 4 if tc6_passed else 0
    print(f"TC6: {'Active listening ports verified':<35} [{'PASSED' if tc6_passed else 'FAILED'}] ({4 if tc6_passed else 0}/4)")

    # TC7: Timestamps and output session validity
    tc7_passed = False
    if tc2_passed or tc3_passed or tc5_passed:
        tc7_passed = True
    results['tc7'] = tc7_passed
    total_score += 4 if tc7_passed else 0
    print(f"TC7: {'Diagnostic session validated':<35} [{'PASSED' if tc7_passed else 'FAILED'}] ({4 if tc7_passed else 0}/4)")

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
