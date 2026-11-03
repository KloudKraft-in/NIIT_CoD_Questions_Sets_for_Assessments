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

    # Technology-Specific Validation Harness for STG_W01_E
    # Persistent NFS Client Mount & /etc/fstab Configuration
    candidate_paths = [
        os.path.join(base_path, 'nfs_mount_report.json'),
        os.path.join(base_path, 'nfs_mount_config.json'),
        os.path.join(base_path, 'nfs_mount_report.txt'),
        os.path.join(os.path.dirname(base_path), 'nfs_mount_report.json'),
        os.path.join(os.path.dirname(base_path), 'nfs_mount_config.json'),
        os.path.expanduser('~/nfs_mount_report.json'),
        '/home/LabsKraft/nfs_mount_report.json',
        '/home/ubuntu/nfs_mount_report.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_report_data(target_file)

            # TC1: Mount point setup: directory /mnt/app_shared exists with proper ownership and permission attributes
            local_mount = str(report.get('local_mount_point', '')).strip()
            permissions = str(report.get('mount_point_permissions', '')).strip()
            system_dir_ok = os.path.isdir('/mnt/app_shared')

            if ('TODO' not in permissions.upper() and 'TODO' not in local_mount.upper()):
                if ('/mnt/app_shared' in local_mount and any(p in permissions for p in ['755', '0755', '775', '0775', 'rwxr'])) or system_dir_ok:
                    results['tc1'] = True

            # TC2: fstab syntax: /etc/fstab contains valid entry with critical network safety options (_netdev, nofail)
            fs_type = str(report.get('filesystem_type', '')).strip().lower()
            fstab_opts = str(report.get('fstab_mount_options', '')).strip().lower()
            fstab_entry = str(report.get('fstab_entry_line', '')).strip()

            system_fstab_ok = False
            if os.path.exists('/etc/fstab'):
                try:
                    with open('/etc/fstab', 'r') as f:
                        fstab_content = f.read()
                    if ('/mnt/app_shared' in fstab_content or '192.168.10.50' in fstab_content) and ('_netdev' in fstab_content) and ('nofail' in fstab_content):
                        system_fstab_ok = True
                except Exception:
                    pass

            report_fstab_ok = False
            if 'TODO' not in fstab_opts.upper() and ('_netdev' in fstab_opts and 'nofail' in fstab_opts):
                if ('nfs' in fs_type or 'nfs' in fstab_entry.lower()) and ('/mnt/app_shared' in fstab_entry or '/mnt/app_shared' in local_mount):
                    report_fstab_ok = True

            if ('TODO' not in fstab_opts.upper() and 'TODO' not in fstab_entry.upper()):
                if report_fstab_ok or system_fstab_ok:
                    results['tc2'] = True

            # TC3: Mount verification: mount command confirms active mount and test file creation succeeds inside /mnt/app_shared
            active_mount = str(report.get('active_mount_verified', '')).strip().upper()
            test_file = str(report.get('test_file_created', '')).strip().upper()
            mount_status = str(report.get('mount_status', '')).strip().upper()

            system_mount_ok = False
            if os.path.exists('/proc/mounts'):
                try:
                    with open('/proc/mounts', 'r') as f:
                        mounts_content = f.read()
                    if '/mnt/app_shared' in mounts_content and 'nfs' in mounts_content:
                        system_mount_ok = True
                except Exception:
                    pass

            report_mount_ok = False
            if ('TODO' not in active_mount and any(s in active_mount for s in ['YES', 'TRUE'])) and \
               ('TODO' not in test_file and any(s in test_file for s in ['YES', 'TRUE'])) and \
               ('TODO' not in mount_status and any(s in mount_status for s in ['SUCCESS', 'MOUNTED', 'RESOLVED', 'ACTIVE', 'OK'])):
                report_mount_ok = True

            if ('TODO' not in active_mount and 'TODO' not in test_file and 'TODO' not in mount_status):
                if report_mount_ok or system_mount_ok:
                    results['tc3'] = True
        except Exception:
            pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (4 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
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
    score = (3 if results.get('tc1') else 0) + (4 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
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
        "tc1": "Mount point setup: directory /mnt/app_shared exists with proper ownership and permission attributes",
        "tc2": "fstab syntax: /etc/fstab contains valid entry with critical network safety options (_netdev, nofail)",
        "tc3": "Mount verification: mount command confirms active mount and test file creation succeeds inside /mnt/app_shared"
    }
    TC_MARKS = {
        "tc1": 3,
        "tc2": 4,
        "tc3": 3
    }

    print("Running Auto-Evaluation for: Storage Lab: Persistent NFS Client Mount & /etc/fstab Configuration\n")
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
