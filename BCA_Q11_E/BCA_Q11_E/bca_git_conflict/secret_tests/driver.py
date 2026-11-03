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
        "tc3": False
    }
    
    ws_path = get_base_path()
    sol_path = os.path.join(ws_path, 'solution.json')
    if not os.path.exists(sol_path):
        return results

    try:
        with open(sol_path, 'r') as f:
            data = json.load(f)
            results['tc1'] = True
    except Exception:
        return results

    branch = str(data.get('conflicting_branch', '') or data.get('branch', '') or data.get('conflicting_branch_name', '')).strip().lower()
    if 'feature/login' in branch or branch == 'feature/login':
        results['tc2'] = True
    else:
        for v in data.values():
            if isinstance(v, str) and 'feature/login' in v.lower():
                results['tc2'] = True
                break

    conflict_file = str(data.get('conflict_file', '') or data.get('file', '') or data.get('conflict_marker_file', '')).strip().lower()
    if 'auth.js' in conflict_file or conflict_file == 'auth.js':
        results['tc3'] = True
    else:
        for v in data.values():
            if isinstance(v, str) and 'auth.js' in v.lower():
                results['tc3'] = True
                break

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (4 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
    
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 30,
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
    
    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        existing_data = {}
        if os.path.exists(sol_path):
            with open(sol_path, 'r') as f:
                existing_data = json.load(f)
        
        score = (3 if test_results.get('tc1') else 0) + (4 if test_results.get('tc2') else 0) + (3 if test_results.get('tc3') else 0)
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
            "tc1": "solution.json exists in student_workspace/",
            "tc2": "Conflicting branch name ('feature/login') identified",
            "tc3": "Conflict marker file ('auth.js') correctly identified"
        }
        print("Running Auto-Evaluation for: Basic Code Analysis: Resolving Merge Conflicts\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 3
            elif k == 'tc2':
                marks = 4
            elif k == 'tc3':
                marks = 3
            else:
                marks = 0

            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/10.0")
