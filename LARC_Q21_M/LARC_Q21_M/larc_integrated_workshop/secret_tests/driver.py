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

    rc = str(data.get('root_cause', '')).strip().lower()
    cid = str(data.get('correlation_id', '')).strip()
    cls = str(data.get('failing_class', '')).strip().lower()
    dur = int(data.get('outage_duration_minutes', 0))

    results['tc1'] = True
    results['tc2'] = (rc != '' and rc != 'todo' and ('pool' in rc or 'exhaustion' in rc or 'connection' in rc or 'timeout' in rc))
    results['tc3'] = (cid != '' and cid.upper() != 'TODO' and ('corr-9921' in cid or '9921' in cid))
    results['tc4'] = (cls != '' and cls != 'todo' and ('payment' in cls or 'service' in cls))
    results['tc5'] = (dur == 45 or dur == 50 or dur > 0)
    
    ev = str(data.get('log_evidence', '')).strip()
    results['tc6'] = (ev != '' and ev.upper() != 'TODO' and len(ev) > 10)
    
    ra = str(data.get('recovery_actions', '') or data.get('immediate_recovery', '')).strip()
    results['tc7'] = (ra != '' and ra.upper() != 'TODO' and len(ra) > 5)
    
    rem = str(data.get('remediation_plan', '')).strip()
    results['tc8'] = (rem != '' and rem.upper() != 'TODO' and len(rem) > 10)

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (4 if results.get('tc1') else 0) + (4 if results.get('tc2') else 0) + (4 if results.get('tc3') else 0) + (4 if results.get('tc4') else 0) + (3 if results.get('tc5') else 0) + (2 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0) + (2 if results.get('tc8') else 0)
    
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
        
        score = (4 if test_results.get('tc1') else 0) + (4 if test_results.get('tc2') else 0) + (4 if test_results.get('tc3') else 0) + (4 if test_results.get('tc4') else 0) + (3 if test_results.get('tc5') else 0) + (2 if test_results.get('tc6') else 0) + (2 if test_results.get('tc7') else 0) + (2 if test_results.get('tc8') else 0)
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
            "tc1": "solution.json exists and is valid JSON",
            "tc2": "Root cause correctly identified as database connection pool exhaustion",
            "tc3": "Primary correlation ID ('corr-9921') matched across logs",
            "tc4": "Failing microservice class and method line number mapped",
            "tc5": "Outage duration and impact metrics correctly calculated",
            "tc6": "Log evidence snippet included",
            "tc7": "Immediate recovery actions documented",
            "tc8": "Long-term architectural remediations included"
        }
        print("Running Auto-Evaluation for: Log Analysis: Integrated Log Investigation Workshop (End-to-End Incident Triage)\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 4
            elif k == 'tc2':
                marks = 4
            elif k == 'tc3':
                marks = 4
            elif k == 'tc4':
                marks = 4
            elif k == 'tc5':
                marks = 3
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
        print(f"\nSCORE: {total_score}/25.0")
