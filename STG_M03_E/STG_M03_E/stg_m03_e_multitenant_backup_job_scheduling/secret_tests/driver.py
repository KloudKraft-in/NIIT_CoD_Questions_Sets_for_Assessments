import os
import sys
import json
import subprocess
from datetime import datetime, timezone


def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_report_data(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return None

    # Try JSON parsing
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            return {str(k).lower().strip(): str(v).strip() for k, v in data.items()}
    except Exception:
        pass

    # Fallback to key: value text lines
    norm = {}
    for line in content.splitlines():
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            norm[k.strip().lower()] = v.strip()
    return norm if norm else None


def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False}
    base_path = get_base_path()

    candidate_paths = [
        os.path.join(base_path, 'backup_schedule_report.json'),
        os.path.join(base_path, 'backup_report.json'),
        os.path.join(base_path, 'backup_optimization_report.json'),
        os.path.join(base_path, 'schedule_report.json'),
        os.path.join(base_path, 'backup_schedule_report.txt'),
        os.path.join(os.path.dirname(base_path), 'backup_schedule_report.json'),
        os.path.expanduser('~/backup_schedule_report.json'),
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    # Check for safe_backup.sh if present in workspace or environment
    script_candidates = [
        os.path.join(base_path, 'safe_backup.sh'),
        os.path.join(os.path.dirname(base_path), 'safe_backup.sh'),
        os.path.expanduser('~/safe_backup.sh'),
        os.path.expanduser('~/NIIT_Workspace/STG_M03_E/stg_m03_e_multitenant_backup_job_scheduling/student_workspace/safe_backup.sh'),
        '/home/LabsKraft/NIIT_Workspace/STG_M03_E/stg_m03_e_multitenant_backup_job_scheduling/student_workspace/safe_backup.sh',
        '/home/LabsKraft/safe_backup.sh',
        'safe_backup.sh'
    ]
    script_content = ""
    for sp in script_candidates:
        if os.path.exists(sp) and os.path.isfile(sp):
            try:
                with open(sp, 'r', encoding='utf-8') as sf:
                    content = sf.read().lower()
                    if content:
                        script_content = content
                        break
            except Exception:
                pass

    if target_file:
        try:
            report = parse_report_data(target_file)
            if report:
                def get_val(keys):
                    for k in keys:
                        for rk, rv in report.items():
                            if k in rk:
                                return rv
                    return ""

                # TC1: Schedule conflict detection: accurately identify the 01:00 AM race condition between snapshot and archive jobs (3 Marks)
                jobs = get_val(['conflicting_jobs', 'conflict_jobs', 'jobs']).lower()
                ctime = get_val(['conflict_time', 'time', 'race_time']).lower()
                vol = get_val(['shared_target_volume', 'target_volume', 'volume']).lower()

                tc1_valid = False
                if 'todo' not in jobs and 'todo' not in ctime:
                    jobs_ok = 'snapshot' in jobs and 'archive' in jobs
                    time_ok = any(t in ctime for t in ['01:00', '1:00', '1am', '0100'])
                    vol_ok = any(v in vol for v in ['lv_data', 'vg_app', 'data']) or not vol
                    if (jobs_ok and time_ok) or (jobs_ok and vol_ok and ('01' in ctime or '1' in ctime)):
                        tc1_valid = True
                if tc1_valid:
                    results['tc1'] = True

                # TC2: Window optimization: cron schedule adjusted to separate jobs based on observed completion times (2 Marks)
                snap_cron = get_val(['snapshot_job_cron', 'snapshot_cron', 'snap_cron']).lower()
                arch_cron = get_val(['rescheduled_archive_cron', 'archive_cron', 'rescheduled_cron', 'archive']).lower()
                buf_min = get_val(['buffer_safety_minutes', 'buffer_minutes', 'buffer']).lower()

                tc2_valid = False
                if 'todo' not in arch_cron and 'todo' not in buf_min:
                    # Snapshot completes in 82 mins (by 02:22). Rescheduled archive should run at or after 02:30 (e.g., 02:30, 03:00, 02:45)
                    arch_ok = any(x in arch_cron for x in ['2', '3', '4', '02:', '03:', '04:'])
                    buf_ok = any(c.isdigit() for c in buf_min) or any(x in buf_min for x in ['min', 'buffer'])
                    if arch_ok and buf_ok:
                        tc2_valid = True
                if tc2_valid:
                    results['tc2'] = True

                # TC3: Advisory lock specification: flock advisory locking mechanism and lockfile path formulated (3 Marks)
                lock_util = get_val(['locking_utility', 'utility', 'lock_type']).lower()
                lock_path = get_val(['lock_file_path', 'lock_file', 'lockfile']).lower()

                tc3_report_ok = ('todo' not in lock_util and 'flock' in lock_util) and ('todo' not in lock_path and 'lock' in lock_path)
                tc3_script_ok = ('flock' in script_content and any(x in script_content for x in ['lock', '-n', '-x', '200']))
                if tc3_report_ok or tc3_script_ok:
                    results['tc3'] = True

                # TC4: Verification test: verify concurrent lock contention behavior and validate clean exit with warning (2 Marks)
                lock_test = get_val(['concurrent_lock_test', 'lock_test', 'test_result', 'concurrent_test']).lower()
                exit_status = get_val(['second_instance_exit_status', 'exit_status', 'warning_status', 'status']).lower()

                report_test_ok = ('todo' not in lock_test and any(x in lock_test for x in ['pass', 'success', 'true', 'ok', 'clean', 'warn', 'handled', 'yes', '1']))
                report_status_ok = ('todo' not in exit_status and any(x in exit_status for x in ['clean', 'warn', 'handled', 'exit', '1', 'pass', 'ok', '0', 'success', 'yes', 'blocked']))
                script_warn_ok = (bool(script_content) and any(x in script_content for x in ['warn', 'already running', 'exit 1', 'exit', 'flock', 'lock']))

                has_attempted = results.get('tc1', False) or results.get('tc2', False) or results.get('tc3', False)

                if report_test_ok and report_status_ok:
                    results['tc4'] = True
                elif (report_test_ok or report_status_ok or script_warn_ok) and has_attempted:
                    results['tc4'] = True
        except Exception:
            pass
    else:
        # Fallback to solution.json if report file is not found
        sol_json = os.path.join(base_path, 'solution.json')
        if os.path.exists(sol_json):
            try:
                with open(sol_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for k in results.keys():
                    if k in data.get('results', {}):
                        results[k] = bool(data['results'][k])
                    elif k in data:
                        results[k] = bool(data[k])
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
        "tc1": "Schedule conflict detection: accurately identify the 01:00 AM race condition between snapshot and archive jobs",
        "tc2": "Window optimization: cron schedule adjusted to separate jobs based on observed completion times",
        "tc3": "Advisory lock specification: flock advisory locking mechanism and lockfile path formulated to prevent concurrent collisions",
        "tc4": "Verification test: verify concurrent lock contention behavior and validate clean exit with warning"
    }
    TC_MARKS = {
        "tc1": 3,
        "tc2": 2,
        "tc3": 3,
        "tc4": 2
}

    print("Running Auto-Evaluation for: Storage Lab: Multi-Tenant Backup Job Scheduling & Lock Conflict Resolution\n")
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
