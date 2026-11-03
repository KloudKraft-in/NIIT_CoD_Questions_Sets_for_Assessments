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
        "tc4": False
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

    cnt = int(data.get('threshold_count', 0))
    win = int(data.get('window_seconds', 0))
    flt = data.get('filter_condition', '').strip().lower()
    results['tc1'] = True
    results['tc2'] = (cnt == 10)
    results['tc3'] = (win == 300 or win == 5)
    results['tc4'] = ('5' in flt or 'error' in flt or 'status' in flt)


    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (2 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0)
    
    # Save solution data for central evaluation registry
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 45,
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
        
        score = (3 if test_results.get('tc1') else 0) + (3 if test_results.get('tc2') else 0) + (2 if test_results.get('tc3') else 0) + (2 if test_results.get('tc4') else 0)
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
            "tc2": "Threshold count set to 10",
            "tc3": "Evaluation window set to 5 minutes (300 seconds)",
            "tc4": "Log filter condition matches HTTP 5xx errors"
        }
        print("Running Auto-Evaluation for: Log Analysis: Log-to-Metric Rule & Alerting Thresholds\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 3
            elif k == 'tc2':
                marks = 3
            elif k == 'tc3':
                marks = 2
            elif k == 'tc4':
                marks = 2
            elif k == 'tc5':
                marks = 0
            elif k == 'tc6':
                marks = 0
            elif k == 'tc7':
                marks = 0
            elif k == 'tc8':
                marks = 0
            else:
                marks = 0

            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/10.0")
