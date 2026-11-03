import os
import sys
import json
import re
from datetime import datetime, timezone

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_report_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try json first
    try:
        data = json.loads(content)
        norm = {str(k).lower().strip(): v for k, v in data.items()}
        return norm
    except Exception:
        pass

    # Fallback to key: value text lines
    norm = {}
    for line in content.splitlines():
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            norm[k.strip().lower()] = v.strip()
    return norm

def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False}
    base_path = get_base_path()

    # Technology-Specific Validation Harness for STG_W02_E
    # SMB/CIFS Network Share Mount with Secure Credentials File
    candidate_paths = [
        os.path.join(base_path, 'cifs_mount_report.json'),
        os.path.join(base_path, 'smb_mount_report.json'),
        os.path.join(base_path, 'cifs_mount_report.txt'),
        os.path.join(os.path.dirname(base_path), 'cifs_mount_report.json'),
        os.path.join(os.path.dirname(base_path), 'smb_mount_report.json'),
        os.path.expanduser('~/cifs_mount_report.json'),
        '/home/LabsKraft/cifs_mount_report.json',
        '/home/ubuntu/cifs_mount_report.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_report_data(target_file)

            # TC1: Credentials security: credentials file created with strict 0600 permissions and valid username/password format
            cred_perm = str(report.get('credentials_file_permissions', '')).strip()
            cred_user = str(report.get('credentials_service_user', '')).strip()

            system_cred_ok = False
            if os.path.exists('/etc/cifs_credentials/smb_finance.cred'):
                try:
                    mode = oct(os.stat('/etc/cifs_credentials/smb_finance.cred').st_mode)[-3:]
                    if mode in ['600', '400']:
                        system_cred_ok = True
                except Exception:
                    pass

            report_cred_ok = False
            if cred_perm and cred_user and ('TODO' not in cred_perm.upper()) and ('TODO' not in cred_user.upper()):
                perm_ok = any(p in cred_perm for p in ['600', '0600', 'rw-------'])
                user_ok = any(u in cred_user.lower() for u in ['svc_fin_app', 'svc', 'user'])
                if perm_ok and (user_ok or system_cred_ok):
                    report_cred_ok = True

            if report_cred_ok:
                results['tc1'] = True

            # TC2: fstab configuration: CIFS entry uses credentials= parameter and modern protocol version vers=3.0
            fstab_opts = str(report.get('fstab_mount_options', '')).strip().lower()
            fstab_line = str(report.get('fstab_entry_line', '')).strip().lower()
            vers = str(report.get('smb_protocol_version', '')).strip().lower()

            system_fstab_ok = False
            if os.path.exists('/etc/fstab'):
                try:
                    with open('/etc/fstab', 'r') as f:
                        fstab_content = f.read().lower()
                    if ('credentials=' in fstab_content) and ('vers=3.0' in fstab_content or 'vers=3' in fstab_content) and ('cifs' in fstab_content):
                        system_fstab_ok = True
                except Exception:
                    pass

            report_fstab_ok = False
            if fstab_opts and ('TODO' not in fstab_opts.upper()):
                opts_ok = 'credentials=' in fstab_opts and ('3.0' in fstab_opts or '3.0' in vers or '3' in vers)
                line_ok = ('cifs' in fstab_line or 'finance' in fstab_line or 'smb' in fstab_line)
                if opts_ok or (system_fstab_ok and ('TODO' not in fstab_line.upper())):
                    report_fstab_ok = True

            if report_fstab_ok:
                results['tc2'] = True

            # TC3: Share reachability: successful mount to /mnt/finance_share verified via mount and df output
            active_mount = str(report.get('active_mount_verified', '')).strip().upper()
            share_read = str(report.get('share_read_verified', '')).strip().upper()
            mount_status = str(report.get('mount_status', '')).strip().upper()

            system_mount_ok = False
            if os.path.exists('/proc/mounts'):
                try:
                    with open('/proc/mounts', 'r') as f:
                        mounts_content = f.read()
                    if '/mnt/finance_share' in mounts_content and 'cifs' in mounts_content:
                        system_mount_ok = True
                except Exception:
                    pass

            report_mount_ok = False
            if ('TODO' not in active_mount) and ('TODO' not in share_read) and ('TODO' not in mount_status):
                active_ok = any(s in active_mount for s in ['YES', 'TRUE'])
                read_ok = any(s in share_read for s in ['YES', 'TRUE'])
                status_ok = any(s in mount_status for s in ['SUCCESS', 'MOUNTED', 'RESOLVED', 'ACTIVE', 'OK'])
                if (active_ok and status_ok) or (system_mount_ok and status_ok):
                    report_mount_ok = True

            if report_mount_ok:
                results['tc3'] = True
        except Exception:
            pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (4 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
    total_marks = 10
    
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 30,
        'evaluation_type': 'AUTO_EVALUATION',
        'score': score,
        'total_marks': total_marks,
        'results': results,
        'exam_code': exam_code
    }
    
    try:
        ws_path = get_base_path()
        with open(os.path.join(ws_path, 'solution.json'), 'w', encoding='utf-8') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[SYSTEM] Warning: Could not write solution.json: {e}")
        
    return score, total_marks, results

if __name__ == "__main__":
    results = run_tests()
    score = (4 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
    total_marks = 10
    
    # Update local solution.json with latest evaluation result
    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        existing_data = {}
        if os.path.exists(sol_path):
            with open(sol_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        existing_data['score'] = score
        existing_data['total_marks'] = total_marks
        existing_data['results'] = results
        with open(sol_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4)
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results))
        sys.exit(0 if score == total_marks else 1)

    TC_NAMES = {
        "tc1": "Credentials security: credentials file created with strict 0600 permissions and valid username/password format",
        "tc2": "fstab configuration: CIFS entry uses credentials= parameter and modern protocol version vers=3.0",
        "tc3": "Share reachability: successful mount to /mnt/finance_share verified via mount and df output"
    }
    TC_MARKS = {
        "tc1": 4,
        "tc2": 3,
        "tc3": 3
    }

    print("Running Auto-Evaluation for: Storage Lab: SMB/CIFS Network Share Mount with Secure Credentials File\n")
    for k, v in results.items():
        tc_num = k[2:]
        desc = TC_NAMES.get(k, '')
        marks = TC_MARKS.get(k, 0)
        display_marks = int(marks) if marks % 1 == 0 else marks
        if v:
            print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
        else:
            print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")

    display_score = int(score) if score % 1 == 0 else score
    display_max = int(total_marks) if total_marks % 1 == 0 else total_marks
    print(f"\nSCORE: {display_score}/{display_max}")
    sys.exit(0 if score == total_marks else 1)
