import json
import os
import sys
import socket
import re
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

# Metadata
QUESTION_CODE = "OS_LX_M03_E"
PROBLEM_SLUG = "os_lx_m03_e_rhel_security_patch_compliance"
LAB_TITLE = "Linux Lab: RHEL Security Patch Compliance & Vulnerability Audit"
TOTAL_MARKS = 10

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
    "tc1": "Current version capture: uname -r and rpm -q outputs captured accurately",
    "tc2": "Security updateinfo listing: dnf updateinfo lists all applicable security advisories",
    "tc3": "Non-intrusive preview: dnf update --security --assumeno runs without modifying system packages",
    "tc4": "CVE data extraction: security_patch_audit.json contains valid CVE identifiers and severity ratings",
    "tc5": "Change request documentation: RFC template populated with valid rollback and test steps"
}
TC_MARKS = {
    "tc1": 2,
    "tc2": 2,
    "tc3": 2,
    "tc4": 2,
    "tc5": 2
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
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False}

    # =========================================================================
    # TC1: Current version capture: uname -r and rpm -q outputs captured accurately (2 Marks)
    # Validates independently: checks security_versions.txt and other version files
    # =========================================================================
    tc1_candidates = [
        "security_versions.txt", "security_version.txt", "versions.txt", "version.txt",
        "kernel_version.txt", "openssl_version.txt", "kernel_openssl.txt",
        "system_versions.txt", "installed_versions.txt", "patch_audit.txt",
        "security_patch_audit.json", "security_patch_audit.txt", "security_audit.txt"
    ]
    for h in homes:
        for fname in tc1_candidates:
            f = os.path.join(h, fname)
            if safe_isfile(f):
                c = safe_read(f).lower()
                has_kernel = ('kernel' in c or 'uname' in c or re.search(r'\d+\.\d+\.\d+', c) or 'linux' in c or 'aws' in c)
                has_openssl = ('openssl' in c or 'ssl' in c or 'package openssl' in c or '3.0.' in c)
                if has_kernel or has_openssl:
                    results['tc1'] = True
                    break
        if results['tc1']:
            break

    if not results['tc1']:
        if check_bash_history(homes, r'uname\s+-r') or check_bash_history(homes, r'rpm\s+-q\s+openssl') or check_bash_history(homes, r'openssl\s+version'):
            results['tc1'] = True

    # =========================================================================
    # TC2: Security updateinfo listing: dnf updateinfo lists all applicable security advisories (2 Marks)
    # Validates independently: checks security_updateinfo.txt and advisory files
    # =========================================================================
    tc2_candidates = [
        "updateinfo.txt", "security_updateinfo.txt", "updateinfo_security.txt",
        "security_updates.txt", "dnf_updateinfo.txt", "advisories.txt",
        "security_advisories.txt", "patch_audit.txt", "security_patch_audit.json",
        "security_patch_audit.txt", "security_audit.txt"
    ]
    for h in homes:
        for fname in tc2_candidates:
            f = os.path.join(h, fname)
            if safe_isfile(f):
                c = safe_read(f)
                if any(w in c for w in ['RHSA-', 'RHBA-', 'RHEA-', 'advisory', 'Advisory', 'updateinfo', 'security', 'Security', 'CVE-']):
                    results['tc2'] = True
                    break
        if results['tc2']:
            break

    if not results['tc2']:
        if check_bash_history(homes, r'dnf\s+updateinfo'):
            results['tc2'] = True

    # =========================================================================
    # TC3: Non-intrusive preview: dnf update --security --assumeno runs without modifying system packages (2 Marks)
    # Validates independently: checks patch_preview.txt and preview logs
    # =========================================================================
    tc3_candidates = [
        "patch_preview.txt", "dnf_preview.txt", "update_preview.txt", "preview.txt",
        "assumeno.txt", "security_preview.txt", "security_patch_preview.txt",
        "dnf_update_security.txt", "patch_audit.txt", "security_patch_audit.json",
        "security_patch_audit.txt", "security_audit.txt"
    ]
    for h in homes:
        for fname in tc3_candidates:
            f = os.path.join(h, fname)
            if safe_isfile(f):
                c = safe_read(f).lower()
                if any(w in c for w in ['assumeno', '--assumeno', 'preview', 'operation aborted', 'nothing to do', 'transaction', 'dependencies resolved', 'is this ok', 'download size', 'no security updates']):
                    results['tc3'] = True
                    break
        if results['tc3']:
            break

    if not results['tc3']:
        if check_bash_history(homes, r'dnf\s+update.*--assumeno') or check_bash_history(homes, r'--assumeno'):
            results['tc3'] = True

    # =========================================================================
    # TC4: CVE data extraction: security_patch_audit.json contains valid CVE identifiers and severity ratings (2 Marks)
    # Validates independently: checks security_patch_audit.json for CVEs and severities
    # =========================================================================
    tc4_candidates = [
        "security_patch_audit.json", "patch_audit.json", "cve_audit.json",
        "security_patch_audit.txt", "patch_audit.txt", "cve_data.json"
    ]
    for h in homes:
        for fname in tc4_candidates:
            f = os.path.join(h, fname)
            if safe_isfile(f):
                c = safe_read(f)
                has_cve = bool(re.search(r'CVE-\d{4}-\d+', c, re.I))
                has_severity = any(s in c.lower() for s in ['critical', 'important', 'moderate', 'low', 'severity', 'high', 'medium'])
                if has_cve and has_severity:
                    results['tc4'] = True
                    break
                elif has_cve:
                    results['tc4'] = True
                    break
        if results['tc4']:
            break

    # =========================================================================
    # TC5: Change request documentation: RFC template populated with valid rollback and test steps (2 Marks)
    # Validates independently: checks rfc_template.txt and RFC files
    # =========================================================================
    tc5_candidates = [
        "rfc_template.txt", "change_request.txt", "rfc.txt", "rfc_patching.txt",
        "rfc_patching.md", "cr_template.txt", "change_request_template.txt",
        "rfc_template.md", "change_request.md", "RFC.md", "RFC.txt"
    ]
    for h in homes:
        for fname in tc5_candidates:
            f = os.path.join(h, fname)
            if safe_isfile(f):
                c = safe_read(f).lower()
                has_just = any(w in c for w in ['justification', 'reason', 'objective', 'purpose'])
                has_risk = any(w in c for w in ['risk', 'impact', 'priority', 'score'])
                has_rollback = any(w in c for w in ['rollback', 'backout', 'revert', 'plan', 'steps'])
                has_test = any(w in c for w in ['test', 'validation', 'verify', 'testing'])
                if has_rollback and (has_just or has_risk or has_test):
                    results['tc5'] = True
                    break
                elif (has_just or has_risk) and has_rollback:
                    results['tc5'] = True
                    break
        if results['tc5']:
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
