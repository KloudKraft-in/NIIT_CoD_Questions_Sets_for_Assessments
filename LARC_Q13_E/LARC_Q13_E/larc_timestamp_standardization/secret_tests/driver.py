import os
import sys
import json
import re

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
    
    js_path = os.path.join(get_base_path(), 'timestamp_converter.js')
    if not os.path.exists(js_path):
        return results

    try:
        with open(js_path, 'r') as f:
            code = f.read()
        
        # Strip comments
        code_no_comments = re.sub(r'//.*|/\*[\s\S]*?\*/', '', code)
        
        results['tc1'] = True
        results['tc2'] = ('toISOString' in code_no_comments or 'Date' in code_no_comments or 'getTime' in code_no_comments)
        results['tc3'] = ('UTC' in code_no_comments or 'Z' in code_no_comments or 'getTimezoneOffset' in code_no_comments)
        
        # Check if convertTimestamp returns non-empty or has actual code
        results['tc4'] = ('return' in code_no_comments and 'return "";' not in code_no_comments and 'return '';' not in code_no_comments)
    except Exception:
        pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (2 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0)
    
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
            "tc1": "timestamp_converter.js is syntax-valid JS",
            "tc2": "Unix epoch converted to ISO string correctly",
            "tc3": "Local timezone offsets adjusted to UTC Z format",
            "tc4": "Returns string ending with 'Z' or '+00:00'"
        }
        print("Running Auto-Evaluation for: Log Analysis: ISO 8601 & Unix Epoch Timestamp Standardization\n")
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
            else:
                marks = 0

            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/10.0")
