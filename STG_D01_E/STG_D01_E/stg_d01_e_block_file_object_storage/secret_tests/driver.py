import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "STG_D01_E"
PROBLEM_SLUG = "stg_d01_e_block_file_object_storage"
LAB_TITLE = "Storage Lab: Block, File & Object Storage Classification & Service Mapping"
TOTAL_MARKS = 10

START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else os.getenv('NIIT_USERNAME', 'LOCAL_USER')
HOME = '/home/Niit' if os.path.isdir('/home/Niit') else os.path.expanduser('~')

def safe_isdir(path):
    if not path:
        return False
    try:
        return os.path.isdir(path)
    except (PermissionError, OSError):
        return False

def safe_isfile(path):
    if not path:
        return False
    try:
        return os.path.isfile(path)
    except (PermissionError, OSError):
        return False

def safe_exists(path):
    if not path:
        return False
    try:
        return os.path.exists(path)
    except (PermissionError, OSError):
        return False

def safe_read(path):
    if not path:
        return ""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except (PermissionError, OSError):
        return ""

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
        except (PermissionError, OSError):
            pass
    ws = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'student_workspace'))
    if safe_isdir(ws):
        homes.add(ws)
    root_ws = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    if safe_isdir(root_ws):
        homes.add(root_ws)
    return list(homes)

def get_search_roots():
    return find_all_user_homes()

def check_home_file(rel_path):
    if not rel_path:
        return None
    trimmed = rel_path.lstrip('~/\\')
    for h in find_all_user_homes():
        p = os.path.join(h, trimmed)
        if safe_isfile(p):
            return p
    return None

def check_system_file(path):
    if not path:
        return None
    return path if safe_isfile(path) else None

def locate_file(path):
    if not path:
        return None
    if path.startswith('~/') or path.startswith('~\\') or not os.path.isabs(path):
        return check_home_file(path)
    return check_system_file(path)

def check_mtime(path):
    if not safe_exists(path):
        return False
    if not START_TIME:
        return True
    try:
        mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
        return mtime >= START_TIME - timedelta(hours=24)
    except Exception:
        return True

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
    "tc1": "Workload classification: accurate categorization of database, shared media, and audit archives across Block, File, and Object models",
    "tc2": "Cross-cloud service mapping: 100% correct mapping to AWS, Azure, and GCP native storage service offerings",
    "tc3": "Artifact generation: ~/storage_mapping.json exists, is valid JSON, and contains protocol details (iSCSI/NVMe, NFS/SMB, HTTPS REST)"
}
TC_MARKS = {
    "tc1": 4,
    "tc2": 3,
    "tc3": 3
}

def run_tests():
    results = {k: False for k in TC_NAMES.keys()}

    # Locate storage_mapping.json across candidate home directories and student workspace
    target_file = locate_file("storage_mapping.json")
    if not target_file or not safe_isfile(target_file):
        return results

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return results

    if not isinstance(data, (dict, list)):
        return results

    raw = json.dumps(data).lower()

    # TC3: Artifact generation: ~/storage_mapping.json exists, is valid JSON, and contains protocol details
    has_block_proto = any(p in raw for p in ['iscsi', 'nvme', 'fibre channel', ' fc '])
    has_file_proto = any(p in raw for p in ['nfs', 'smb', 'cifs'])
    has_obj_proto = any(p in raw for p in ['https', 'rest', 's3 api', 'http'])
    if has_block_proto and has_file_proto and has_obj_proto:
        results['tc3'] = True

    # TC1: Workload classification: accurate categorization of database, shared media, and audit archives across models
    db_block = bool(re.search(r'(database|oracle|datafile|db).{1,120}block|block.{1,120}(database|oracle|datafile|db)', raw, re.DOTALL))
    media_file = bool(re.search(r'(media|upload|shared|web).{1,120}file|file.{1,120}(media|upload|shared|web)', raw, re.DOTALL))
    audit_obj = bool(re.search(r'(audit|archive|cold|log).{1,120}object|object.{1,120}(audit|archive|cold|log)', raw, re.DOTALL))
    if db_block and media_file and audit_obj:
        results['tc1'] = True
    elif 'block' in raw and 'file' in raw and 'object' in raw and ('database' in raw or 'oracle' in raw) and ('media' in raw or 'upload' in raw or 'shared' in raw) and ('audit' in raw or 'archive' in raw):
        results['tc1'] = True

    # TC2: Cross-cloud service mapping: 100% correct mapping to AWS, Azure, and GCP native storage service offerings
    aws_ok = ('ebs' in raw) and ('efs' in raw) and ('s3' in raw)
    azure_ok = ('disk' in raw or 'managed disk' in raw) and ('azure file' in raw or 'files' in raw) and ('blob' in raw)
    gcp_ok = ('persistent disk' in raw or 'pd' in raw) and ('filestore' in raw) and ('cloud storage' in raw or 'gcs' in raw)
    if aws_ok and azure_ok and gcp_ok:
        results['tc2'] = True

    return results

def verify_task():
    results = run_tests()
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
            with open(legacy_metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                metadata.update(existing_data)
                existing_data = metadata
    except Exception:
        pass
        
    with open(os.path.join(ws_path, 'solution.json'), 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)
    with open(os.path.join(ws_path, 'solution.py'), 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)
        
    root_ws_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    with open(os.path.join(root_ws_path, 'solution.json'), 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)
    with open(os.path.join(root_ws_path, 'solution.py'), 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)
        
    try:
        if os.path.isdir(os.path.dirname(legacy_metadata_path)):
            with open(legacy_metadata_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=4)
    except Exception:
        pass

if __name__ == "__main__":
    verify_task()
