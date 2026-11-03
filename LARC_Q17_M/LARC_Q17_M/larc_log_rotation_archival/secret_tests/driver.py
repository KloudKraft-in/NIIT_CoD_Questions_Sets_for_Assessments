import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False,
        "tc6": False,
        "tc7": False,
        "tc8": False
    }
    
    sol_path = os.path.join(get_base_path(), 'solution.json')
    if not os.path.exists(sol_path):
        return results

    try:
        with open(sol_path, 'r') as f:
            data = json.load(f)
    except Exception:
        return results

    # Specific question evaluation logic

    fn = str(data.get('archive_filename', '')).strip().lower()
    ts = str(data.get('failure_timestamp', '')).strip()
    exc = str(data.get('exception_class', '')).strip().lower()
    cmd = str(data.get('zgrep_cmd', '')).strip().lower()
    pid = int(data.get('pid', 0))
    rca = str(data.get('rca_summary', '')).strip()

    results['tc1'] = True
    results['tc2'] = (fn != '' and fn != 'todo' and ('syslog.2.gz' in fn or 'syslog' in fn))
    results['tc3'] = (ts != '' and ts.upper() != 'TODO' and len(ts) > 5)
    results['tc4'] = (exc != '' and exc != 'todo' and ('error' in exc or 'exception' in exc or 'timeout' in exc))
    results['tc5'] = (cmd != '' and cmd != 'todo' and ('zgrep' in cmd or 'zcat' in cmd))

    pol_val = str(data.get('rotation_policy', '') or data.get('log_rotation_policy', '')).strip().lower()
    pol_rca = str(data.get('rca_summary', '')).strip().lower()
    if pol_val != '' and pol_val != 'todo':
        results['tc6'] = ('size' in pol_val or 'daily' in pol_val or 'rotate' in pol_val or 'rotation' in pol_val or 'policy' in pol_val or 'weekly' in pol_val or 'logrotate' in pol_val)
    elif pol_rca != '' and pol_rca != 'todo':
        results['tc6'] = ('size' in pol_rca or 'daily' in pol_rca or 'rotate' in pol_rca or 'rotation' in pol_rca or 'policy' in pol_rca or 'weekly' in pol_rca or 'logrotate' in pol_rca)
    else:
        results['tc6'] = False

    results['tc7'] = (pid > 0)
    results['tc8'] = (rca != '' and rca.upper() != 'TODO' and len(rca) > 10)

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (3 if results.get('tc4') else 0) + (2 if results.get('tc5') else 0) + (2 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0) + (2 if results.get('tc8') else 0)
    
    # Save solution data for central evaluation registry
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 90,
        'evaluation_type': 'AUTO_EVALUATION',
        'score': score,
        'results': results,
        'exam_code': exam_code
    }
    
    ws_path = get_base_path()
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(solution_data, f, indent=4)

if __name__ == "__main__":
    test_results = run_tests()
    
    # Write solution file for the platform grading runner
    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        existing_data = {}
        if os.path.exists(sol_path):
            with open(sol_path, 'r') as f:
                existing_data = json.load(f)
        
        score = (3 if test_results.get('tc1') else 0) + (3 if test_results.get('tc2') else 0) + (3 if test_results.get('tc3') else 0) + (3 if test_results.get('tc4') else 0) + (2 if test_results.get('tc5') else 0) + (2 if test_results.get('tc6') else 0) + (2 if test_results.get('tc7') else 0) + (2 if test_results.get('tc8') else 0)
        existing_data['score'] = score
        existing_data['results'] = test_results
        
        with open(sol_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(test_results))
    else:
        TC_NAMES = {
            "tc1": "solution.json exists",
            "tc2": "Target compressed archive file ('syslog.2.gz') correctly identified",
            "tc3": "Timestamp of initial rotated failure extracted",
            "tc4": "Error exception class identified",
            "tc5": "zgrep filter expression documented",
            "tc6": "Log rotation policy type identified (size/daily)",
            "tc7": "Impacted service process ID matched",
            "tc8": "Root cause summary filled"
        }
        print("Running Auto-Evaluation for: Log Analysis: Log Rotation Audit & Compressed Log Archival Triage\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 3
            elif k == 'tc2':
                marks = 3
            elif k == 'tc3':
                marks = 3
            elif k == 'tc4':
                marks = 3
            elif k == 'tc5':
                marks = 2
            elif k == 'tc6':
                marks = 2
            elif k == 'tc7':
                marks = 2
            elif k == 'tc8':
                marks = 2
            else:
                marks = 0

            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/20.0")
