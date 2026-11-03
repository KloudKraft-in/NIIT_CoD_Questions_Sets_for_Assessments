# import os
# import sys
# import json

# def get_base_path():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

# def run_tests():
#     results = {
#         "tc1": False,
#         "tc2": False,
#         "tc3": False
#     }
    
#     sol_path = os.path.join(get_base_path(), 'solution.json')
#     if not os.path.exists(sol_path):
#         return results

#     try:
#         with open(sol_path, 'r') as f:
#             data = json.load(f)
#     except Exception:
#         return results

#     # Specific question evaluation logic

#     js_path = os.path.join(get_base_path(), 'user_lookup.js')
#     if os.path.exists(js_path):
#         with open(js_path, 'r') as f:
#             code = f.read()
#         results['tc1'] = True
#         results['tc2'] = ('undefined' in code or 'null' in code or '?' in code or 'if' in code)
#         results['tc3'] = ('.profile' in code and ('!' in code or '&&' in code or '?' in code))


#     return results

# def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
#     results = run_tests()
#     score = (3 if results.get('tc1') else 0) + (4 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
    
#     # Save solution data for central evaluation registry
#     solution_data = {
#         'candidate_prefix': vm_tag,
#         'assessment_start_time': start_time,
#         'max_duration_minutes': 30,
#         'evaluation_type': 'AUTO_EVALUATION',
#         'score': score,
#         'results': results,
#         'exam_code': exam_code
#     }
    
#     ws_path = get_base_path()
#     with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
#         json.dump(solution_data, f, indent=4)

# if __name__ == "__main__":
#     test_results = run_tests()
    
#     # Write solution file for the platform grading runner
#     try:
#         sol_path = os.path.join(get_base_path(), 'solution.json')
#         existing_data = {}
#         if os.path.exists(sol_path):
#             with open(sol_path, 'r') as f:
#                 existing_data = json.load(f)
        
#         score = (3 if test_results.get('tc1') else 0) + (4 if test_results.get('tc2') else 0) + (3 if test_results.get('tc3') else 0)
#         existing_data['score'] = score
#         existing_data['results'] = test_results
        
#         with open(sol_path, 'w') as f:
#             json.dump(existing_data, f, indent=4)
#     except Exception:
#         pass

#     if len(sys.argv) > 1 and sys.argv[1] == '--json':
#         print(json.dumps(test_results))
#     else:
#         TC_NAMES = {
#             "tc1": "user_lookup.js contains syntax-valid JS code",
#             "tc2": "Code handles non-existent/null user objects correctly",
#             "tc3": "Function returns an empty string or null instead of throwing an error"
#         }
#         print("Running Auto-Evaluation for: Basic Code Analysis: Spotting Logical & Null Errors\n")
#         total_score = 0
#         for k, v in test_results.items():
#             tc_num = k[2:]
#             desc = TC_NAMES.get(k, '')
#             if k == 'tc1':
#                 marks = 3
#             elif k == 'tc2':
#                 marks = 4
#             elif k == 'tc3':
#                 marks = 3
#             elif k == 'tc4':
#                 marks = 0
#             elif k == 'tc5':
#                 marks = 0
#             elif k == 'tc6':
#                 marks = 0
#             elif k == 'tc7':
#                 marks = 0
#             elif k == 'tc8':
#                 marks = 0
#             else:
#                 marks = 0

#             if v:
#                 total_score += marks
#                 print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
#             else:
#                 print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
#         print(f"\nSCORE: {total_score}/10.0")




import os
import sys
import json
import subprocess

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False
    }
    
    js_path = os.path.join(get_base_path(), 'user_lookup.js')
    if not os.path.exists(js_path):
        return results

    eval_script = '''
try {
    const { getUserEmail } = require('./user_lookup.js');
    let tc2 = false;
    let tc3 = false;
    
    try {
        const r1 = getUserEmail(null);
        const r2 = getUserEmail({});
        const r3 = getUserEmail(undefined);
        tc2 = true;
        if ((r1 === '' || r1 === null || r1 === undefined) &&
            (r2 === '' || r2 === null || r2 === undefined)) {
            tc3 = true;
        }
    } catch(e) {
        tc2 = false;
        tc3 = false;
    }

    try {
        const validRes = getUserEmail({ profile: { email: 'alice@example.com' } });
        if (validRes !== 'alice@example.com') {
            tc3 = false;
        }
    } catch(e) {
        tc3 = false;
    }

    console.log(JSON.stringify({ tc1: true, tc2, tc3 }));
} catch(err) {
    console.log(JSON.stringify({ tc1: false, tc2: false, tc3: false }));
}
'''

    try:
        process = subprocess.run(['node', '-e', eval_script], cwd=get_base_path(), capture_output=True, text=True, timeout=10)
        if process.returncode == 0 and process.stdout.strip():
            res = json.loads(process.stdout.strip())
            results['tc1'] = res.get('tc1', False)
            results['tc2'] = res.get('tc2', False)
            results['tc3'] = res.get('tc3', False)
    except Exception:
        pass

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
            "tc1": "user_lookup.js contains syntax-valid JS code",
            "tc2": "Code handles non-existent/null user objects correctly",
            "tc3": "Function returns an empty string or null instead of throwing an error"
        }
        print("Running Auto-Evaluation for: Basic Code Analysis: Spotting Logical & Null Errors\n")
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

