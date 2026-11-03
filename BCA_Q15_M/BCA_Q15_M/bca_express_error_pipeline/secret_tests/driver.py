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

    js_path = os.path.join(get_base_path(), 'app.js')
    if os.path.exists(js_path):
        with open(js_path, 'r') as f:
            code = f.read()
        results['tc1'] = ('(err, req, res, next)' in code.replace(' ', '') or '(err,req,res,next)' in code.replace(' ', ''))
        results['tc2'] = ('stack' not in code.lower() or 'message' in code.lower())
        results['tc3'] = ('console.error' in code or 'logger' in code)
        results['tc4'] = ('status(500)' in code.replace(' ', '') or 'status(500)' in code)


    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (8 if results.get('tc1') else 0) + (8 if results.get('tc2') else 0) + (7 if results.get('tc3') else 0) + (7 if results.get('tc4') else 0)
    
    # Save solution data for central evaluation registry
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 60,
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
        
        score = (8 if test_results.get('tc1') else 0) + (8 if test_results.get('tc2') else 0) + (7 if test_results.get('tc3') else 0) + (7 if test_results.get('tc4') else 0)
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
            "tc1": "Custom middleware function declared with 4 arguments",
            "tc2": "Sanitizes raw SQL queries from the client error response",
            "tc3": "Logs raw details locally to file/console",
            "tc4": "Sends formatted JSON client response with public message"
        }
        print("Running Auto-Evaluation for: Basic Code Analysis: Custom Express Middleware Error Pipelines\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 8
            elif k == 'tc2':
                marks = 8
            elif k == 'tc3':
                marks = 7
            elif k == 'tc4':
                marks = 7
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
        print(f"\nSCORE: {total_score}/30.0")
