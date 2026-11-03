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

    try:
        data = json.loads(content)
        return {str(k).lower().strip(): v for k, v in data.items()}
    except Exception:
        pass

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

    candidate_paths = [
        os.path.join(base_path, 'unresponsive_mount_report.json'),
        os.path.join(base_path, 'unresponsive_mount_triage.json'),
        os.path.join(base_path, 'mount_teardown_report.json'),
        os.path.join(os.path.dirname(base_path), 'unresponsive_mount_report.json'),
        os.path.expanduser('~/unresponsive_mount_report.json'),
        '/home/LabsKraft/unresponsive_mount_report.json',
        '/home/ubuntu/unresponsive_mount_report.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_report_data(target_file)

            # TC1: Mount hung detection: timeout command detects mount freeze without causing diagnostic tool lockup
            detect_cmd = str(report.get('hung_detection_command', '')).strip().lower()
            exit_code = str(report.get('detection_exit_code', '')).strip()
            status = str(report.get('mount_status', '')).strip().upper()

            if ('TODO' not in detect_cmd.upper() and 'timeout' in detect_cmd and 'remote_nfs' in detect_cmd) and \
               ('TODO' not in exit_code and '124' in exit_code) and \
               ('TODO' not in status and 'HUNG' in status):
                results['tc1'] = True

            # TC2: Process termination: fuser cleanly signals processes in D-state holding descriptors to the dead share
            kill_cmd = str(report.get('process_kill_command', '')).strip().lower()
            term_signal = str(report.get('termination_signal', '')).strip().upper()

            if ('TODO' not in kill_cmd.upper() and 'fuser' in kill_cmd and any(s in kill_cmd for s in ['-k', 'kill', 'remote_nfs'])) and \
               ('TODO' not in term_signal and any(s in term_signal for s in ['SIGKILL', '9', 'KILL'])):
                results['tc2'] = True

            # TC3: Lazy unmount execution: umount -l successfully detaches the unresponsive filesystem from directory tree
            umount_cmd = str(report.get('lazy_unmount_command', '')).strip().lower()
            unmount_opt = str(report.get('unmount_option_used', '')).strip().lower()

            if ('TODO' not in umount_cmd.upper() and 'umount' in umount_cmd and any(s in umount_cmd for s in ['-l', 'lazy'])) and \
               ('TODO' not in unmount_opt.upper() and any(s in unmount_opt for s in ['-l', 'lazy'])):
                results['tc3'] = True

            # TC4: State verification: /proc/mounts confirms removal and df operates normally without hanging
            proc_verif = str(report.get('proc_mounts_verification', '')).strip().upper()
            tools_resp = str(report.get('storage_tools_responsive', '')).strip().upper()

            if ('TODO' not in proc_verif and any(s in proc_verif for s in ['REMOVED', 'CLEARED', 'NOT_PRESENT', 'ABSENT', 'YES'])) and \
               ('TODO' not in tools_resp and any(s in tools_resp for s in ['YES', 'TRUE', 'NORMAL', 'RESPONSIVE'])):
                results['tc4'] = True

        except Exception:
            pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (2 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0)
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
    score = (3 if results.get('tc1') else 0) + (2 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0)
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
        "tc1": "Mount hung detection: timeout command detects mount freeze without causing diagnostic tool lockup",
        "tc2": "Process termination: fuser cleanly signals processes in D-state holding descriptors to the dead share",
        "tc3": "Lazy unmount execution: umount -l successfully detaches the unresponsive filesystem from directory tree",
        "tc4": "State verification: /proc/mounts confirms removal and df operates normally without hanging"
    }
    TC_MARKS = {
        "tc1": 3,
        "tc2": 2,
        "tc3": 3,
        "tc4": 2
    }

    print("Running Auto-Evaluation for: Storage Lab: Unresponsive Network Mount Clean Teardown & Process Remediation\n")
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
