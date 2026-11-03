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
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False}
    base_path = get_base_path()

    # Technology-Specific Validation Harness for STG_W05_M
    # Stale NFS Mount Diagnosis & NetApp ONTAP SVM Export Policy Triage
    candidate_paths = [
        os.path.join(base_path, 'stale_nfs_report.json'),
        os.path.join(base_path, 'stale_mount_report.json'),
        os.path.join(base_path, 'stale_nfs_triage.json'),
        os.path.join(base_path, 'stale_nfs_report.txt'),
        os.path.join(os.path.dirname(base_path), 'stale_nfs_report.json'),
        os.path.expanduser('~/stale_nfs_report.json'),
        '/home/LabsKraft/stale_nfs_report.json',
        '/home/ubuntu/stale_nfs_report.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_report_data(target_file)

            # TC1: Stale mount identification: accurately diagnose ESTALE error condition and identify processes holding locks
            err_code = str(report.get('detected_error_code', '')).strip().upper()
            tool = str(report.get('locking_process_discovery_tool', '')).strip().lower()

            if ('TODO' not in err_code and any(e in err_code for e in ['ESTALE', 'STALE'])) and \
               ('TODO' not in tool.upper() and any(t in tool for t in ['fuser', 'lsof'])):
                results['tc1'] = True

            # TC2: Safe unmount execution: successfully unmount the hung share using umount -l without leaving orphaned kernel states
            umount_cmd = str(report.get('safe_unmount_command', '')).strip().lower()
            avoid_orphan = str(report.get('orphaned_kernel_states_avoided', '')).strip().upper()

            if ('TODO' not in umount_cmd.upper() and 'umount' in umount_cmd and any(k in umount_cmd for k in ['-l', 'lazy'])) and \
               ('TODO' not in avoid_orphan and any(s in avoid_orphan for s in ['YES', 'TRUE'])):
                results['tc2'] = True

            # TC3: NetApp export policy analysis: correctly identify the missing client IP in export_policy_dump.txt as root cause
            subnet = str(report.get('identified_root_cause_subnet', '')).strip()
            remediation = str(report.get('netapp_remediation_rule', '')).strip().lower()

            if ('TODO' not in subnet.upper() and '192.168.20' in subnet) and \
               ('TODO' not in remediation.upper() and ('192.168.20' in remediation or 'export-policy' in remediation)):
                results['tc3'] = True

            # TC4: Successful recovery: remount share successfully and verify read/write transaction completion
            remount_cmd = str(report.get('remount_command_executed', '')).strip().lower()
            rw_verif = str(report.get('read_write_verification', '')).strip().upper()
            status = str(report.get('recovery_status', '')).strip().upper()

            if ('TODO' not in remount_cmd.upper() and 'mount' in remount_cmd and 'netapp_shared' in remount_cmd) and \
               ('TODO' not in rw_verif and any(s in rw_verif for s in ['YES', 'TRUE'])) and \
               ('TODO' not in status and any(s in status for s in ['SUCCESS', 'RESOLVED', 'ACTIVE', 'OK'])):
                results['tc4'] = True
        except Exception:
            pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (5 if results.get('tc1') else 0) + (5 if results.get('tc2') else 0) + (5 if results.get('tc3') else 0) + (5 if results.get('tc4') else 0)
    total_marks = 20
    
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 60,
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
    score = (5 if results.get('tc1') else 0) + (5 if results.get('tc2') else 0) + (5 if results.get('tc3') else 0) + (5 if results.get('tc4') else 0)
    total_marks = 20
    
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
        "tc1": "Stale mount identification: accurately diagnose ESTALE error condition and identify processes holding locks",
        "tc2": "Safe unmount execution: successfully unmount the hung share using umount -l without leaving orphaned kernel states",
        "tc3": "NetApp export policy analysis: correctly identify the missing client IP in export policy dump as root cause",
        "tc4": "Successful recovery: remount share successfully and verify read/write transaction completion"
    }
    TC_MARKS = {
        "tc1": 5,
        "tc2": 5,
        "tc3": 5,
        "tc4": 5
    }

    print("Running Auto-Evaluation for: Storage Lab: Stale NFS Mount Diagnosis & NetApp ONTAP SVM Export Policy Triage\n")
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
