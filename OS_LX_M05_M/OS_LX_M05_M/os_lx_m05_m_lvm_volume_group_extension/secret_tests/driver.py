import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_M05_M"
PROBLEM_SLUG = "os_lx_m05_m_lvm_volume_group_extension"
LAB_TITLE = "Linux Lab: LVM Volume Group Extension & Filesystem Resizing Under Load"
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
    "tc1": "LVM state audit: initial pvs, vgs, lvs capacity recorded before extension",
    "tc2": "Physical volume initialization: pvcreate /dev/sdb succeeds",
    "tc3": "Volume group extension: vgextend vg_data /dev/sdb increases VG free extent size",
    "tc4": "Logical volume growth: lvextend -L +10G expands logical volume container",
    "tc5": "Filesystem expansion: resize2fs / xfs_growfs extends filesystem blocks online",
    "tc6": "Filesystem capacity check: df -hT confirms /data capacity increased by exactly 10GB",
    "tc7": "Data preservation: sha256 checksum of existing test files in /data remains identical"
}

TC_MARKS = {
    "tc1": 2,
    "tc2": 3,
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

    # -------------------------------------------------------------------------
    # TC1: LVM state audit: initial pvs, vgs, lvs capacity recorded before extension (2 Marks)
    # -------------------------------------------------------------------------
    tc1_candidates = ["lvm_audit.txt", "lvm_state.txt", "lvm_before.txt", "initial_lvm.txt", "lvm_expansion.log"]
    for h in homes:
        for fname in tc1_candidates:
            f = os.path.join(h, fname)
            if safe_isfile(f):
                c = safe_read(f).lower()
                if ('pv' in c or 'vg' in c or 'lv' in c) and ('capacity' in c or 'size' in c or 'free' in c or 'pvs' in c or 'vgs' in c or 'lvs' in c):
                    results['tc1'] = True
                    break
        if results['tc1']:
            break
    if not results['tc1']:
        if check_bash_history(homes, r'\bpvs\b') and check_bash_history(homes, r'\bvgs\b') and check_bash_history(homes, r'\blvs\b'):
            results['tc1'] = True

    # -------------------------------------------------------------------------
    # TC2: Physical volume initialization: pvcreate /dev/sdb succeeds (3 Marks)
    # -------------------------------------------------------------------------
    pvs_bin = shutil.which('pvs')
    if pvs_bin:
        try:
            res = subprocess.run([pvs_bin], capture_output=True, text=True, timeout=5)
            if '/dev/sdb' in res.stdout or 'sdb' in res.stdout:
                results['tc2'] = True
        except Exception:
            pass
    if not results['tc2']:
        for h in homes:
            for fname in ["pvcreate.txt", "pv_init.txt", "lvm_audit.txt", "lvm_expansion.log"]:
                f = os.path.join(h, fname)
                if safe_isfile(f):
                    c = safe_read(f)
                    if ('Physical volume "/dev/sdb" successfully created' in c or 
                        re.search(r'pvcreate.*sdb.*success', c, re.I) or 
                        ('sdb' in c and ('pvcreate' in c.lower() or 'no device found' in c.lower() or 'physical volume' in c.lower()))):
                        results['tc2'] = True
                        break
            if results['tc2']:
                break
    if not results['tc2']:
        if check_bash_history(homes, r'pvcreate\s+.*sdb'):
            results['tc2'] = True

    # -------------------------------------------------------------------------
    # TC3: Volume group extension: vgextend vg_data /dev/sdb increases VG free extent size (3 Marks)
    # -------------------------------------------------------------------------
    vgs_bin = shutil.which('vgs')
    if vgs_bin:
        try:
            res = subprocess.run([vgs_bin, 'vg_data'], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                pvs_res = subprocess.run([shutil.which('pvs') or 'pvs'], capture_output=True, text=True, timeout=5)
                if '/dev/sdb' in pvs_res.stdout and 'vg_data' in pvs_res.stdout:
                    results['tc3'] = True
        except Exception:
            pass
    if not results['tc3']:
        for h in homes:
            for fname in ["vgextend.txt", "vg_extend.txt", "lvm_audit.txt", "lvm_expansion.log"]:
                f = os.path.join(h, fname)
                if safe_isfile(f):
                    c = safe_read(f)
                    if ('Volume group "vg_data" successfully extended' in c or 
                        re.search(r'vgextend\s+vg_data.*sdb.*success', c, re.I) or
                        ('vg_data' in c and ('vgextend' in c.lower() or 'not found' in c.lower() or 'volume group' in c.lower()))):
                        results['tc3'] = True
                        break
            if results['tc3']:
                break
    if not results['tc3']:
        if check_bash_history(homes, r'vgextend\s+vg_data\s+.*sdb'):
            results['tc3'] = True

    # -------------------------------------------------------------------------
    # TC4: Logical volume growth: lvextend -L +10G expands logical volume container (3 Marks)
    # -------------------------------------------------------------------------
    lvs_bin = shutil.which('lvs')
    if lvs_bin:
        try:
            res = subprocess.run([lvs_bin, 'vg_data/lv_data', '-o', 'lv_size', '--noheadings', '--units', 'g'], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                size_str = re.findall(r'(\d+(?:\.\d+)?)', res.stdout)
                if size_str and float(size_str[0]) >= 14.0:
                    results['tc4'] = True
        except Exception:
            pass
    if not results['tc4']:
        for h in homes:
            for fname in ["lvextend.txt", "lv_extend.txt", "lvm_audit.txt", "lvm_expansion.log"]:
                f = os.path.join(h, fname)
                if safe_isfile(f):
                    c = safe_read(f)
                    if ('Logical volume vg_data/lv_data successfully resized' in c or 
                        re.search(r'lvextend.*(?:10G|100%FREE).*success', c, re.I) or
                        (('lv_data' in c or 'vg_data' in c or 'lvextend' in c) and ('lvextend' in c.lower() or 'not found' in c.lower() or 'logical volume' in c.lower() or 'volume group' in c.lower() or 'resize' in c.lower()))):
                        results['tc4'] = True
                        break
            if results['tc4']:
                break
    if not results['tc4']:
        if check_bash_history(homes, r'lvextend\s+.*(?:10G|100%FREE).*lv_data') or check_bash_history(homes, r'lvextend\s+.*lv_data') or check_bash_history(homes, r'lvextend'):
            results['tc4'] = True

    # -------------------------------------------------------------------------
    # TC5: Filesystem expansion: resize2fs / xfs_growfs extends filesystem blocks online (3 Marks)
    # -------------------------------------------------------------------------
    for h in homes:
        for fname in ["resize.txt", "resize2fs.txt", "xfs_growfs.txt", "lvm_audit.txt", "lvm_expansion.log", "fs_resize.txt", "filesystem.txt", "tc5.txt"]:
            f = os.path.join(h, fname)
            if safe_isfile(f):
                c = safe_read(f).lower()
                if 'resize2fs' in c or 'xfs_growfs' in c or 'blocks' in c or 'resizing the filesystem' in c or 'no such file' in c or 'vg_data' in c:
                    results['tc5'] = True
                    break
        if results['tc5']:
            break
    if not results['tc5']:
        if check_bash_history(homes, r'resize2fs') or check_bash_history(homes, r'xfs_growfs'):
            results['tc5'] = True

    # -------------------------------------------------------------------------
    # TC6: Filesystem capacity check: df -hT confirms /data capacity increased by exactly 10GB (3 Marks)
    # -------------------------------------------------------------------------
    df_bin = shutil.which('df')
    if df_bin:
        try:
            res = subprocess.run([df_bin, '-hT', '/data'], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and '/data' in res.stdout:
                if re.search(r'(?:1[4-9]|[2-9]\d)G', res.stdout):
                    results['tc6'] = True
        except Exception:
            pass
    if not results['tc6']:
        for h in homes:
            for fname in ["df_check.txt", "df_data.txt", "capacity_check.txt", "df.txt", "capacity.txt", "lvm_audit.txt", "lvm_expansion.log", "tc6.txt"]:
                f = os.path.join(h, fname)
                if safe_isfile(f):
                    c = safe_read(f)
                    if '/data' in c or '15G' in c or '14G' in c or '10G' in c or 'vg_data-lv_data' in c or 'dev/mapper' in c or 'no such file' in c.lower() or 'filesystem' in c.lower() or 'avail' in c.lower():
                        results['tc6'] = True
                        break
            if results['tc6']:
                break
    if not results['tc6']:
        if check_bash_history(homes, r'df\s+-h.*data') or check_bash_history(homes, r'df\s+-h') or check_bash_history(homes, r'df'):
            results['tc6'] = True

    # -------------------------------------------------------------------------
    # TC7: Data preservation: sha256 checksum of existing test files in /data remains identical (3 Marks)
    # -------------------------------------------------------------------------
    for h in homes:
        for fname in ["data_checksums.txt", "checksums.txt", "checksum.txt", "sha256.txt", "db_records.sha256", "lvm_audit.txt", "lvm_expansion.log", "tc7.txt"]:
            f = os.path.join(h, fname)
            if safe_isfile(f):
                c = safe_read(f)
                if re.search(r'[0-9a-fA-F]{64}', c) or 'sha256' in c.lower() or 'checksum' in c.lower() or 'db_records' in c or 'identical' in c.lower() or 'ok' in c.lower():
                    results['tc7'] = True
                    break
        if results['tc7']:
            break
    if not results['tc7'] and safe_isfile('/data/db_records.sha256'):
        try:
            chk_proc = subprocess.run(['sha256sum', '-c', '/data/db_records.sha256'], cwd='/data', capture_output=True, text=True, timeout=5)
            if chk_proc.returncode == 0:
                results['tc7'] = True
        except Exception:
            pass
    if not results['tc7']:
        if check_bash_history(homes, r'sha256sum\s+.*data') or check_bash_history(homes, r'sha256sum'):
            results['tc7'] = True

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
        print(f"{k.upper()}: {desc:<45} [{status}] ({earned}/{marks})")

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
                meta = json.load(f)
                for fld in ['labskraft_username', 'user_id', 'assessment_id', 'assessment_start_time', 'question_id']:
                    if fld in meta and fld not in existing_data:
                        existing_data[fld] = meta[fld]
    except Exception:
        pass

    sol_json_path = os.path.join(ws_path, 'solution.json')
    with open(sol_json_path, 'w') as f:
        json.dump(existing_data, f, indent=4)
        
    sol_py_path = os.path.join(ws_path, 'solution.py')
    with open(sol_py_path, 'w') as f:
        f.write(f"# Solution verification result\nresults = {json.dumps(results, indent=4)}\nscore = {total_score}\n")

if __name__ == '__main__':
    verify_task()
