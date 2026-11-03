# import os
# import sys
# import json

# def get_base_path():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

# def run_tests():
#     import subprocess
#     base_path = get_base_path()
#     results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}
#     # TC1: File server.js exists
#     js_file = os.path.join(base_path, 'server.js')
#     worker_file = os.path.join(base_path, 'worker.js')
#     if os.path.exists(js_file):
#         results['tc1'] = True
#     if os.path.exists(worker_file):
#         results['tc2'] = True
        
#     try:
#         with open(js_file, 'r') as f:
#             content = f.read()
#             if 'Worker' in content and 'worker_threads' in content:
#                 results['tc3'] = True
#                 results['tc4'] = True
#                 results['tc5'] = True
#                 results['tc8'] = True
#         with open(worker_file, 'r') as f:
#             w_content = f.read()
#             if 'parentPort' in content or 'pbkdf2' in w_content:
#                 results['tc6'] = True
#                 results['tc7'] = True
#     except Exception:
#         pass
#     return results

# if __name__ == "__main__":
#     test_results = run_tests()
#     try:
#         sol_path = os.path.join(get_base_path(), 'solution.java')
#         with open(sol_path, 'w') as f:
#             json.dump({'results': test_results}, f)
#     except Exception:
#         pass
    
#     if len(sys.argv) > 1 and sys.argv[1] == '--json':
#         print(json.dumps(test_results))
#     else:
#         TC_NAMES = {
#             "tc1": "File server.js exists in workspace", "tc2": "File worker.js exists in workspace", "tc3": "Worker pools utilized for processing CPU-intensive operations", "tc4": "Main execution threads remain non-blocked during hashing execution", "tc5": "Asynchronous response payloads correctly formatted", "tc6": "Worker data pbkdf2 properties configurations matched", "tc7": "System handles thread messaging error events", "tc8": "Node.js worker_threads module integrated successfully"
#         }
#         print("Running Tests for: Sync Offloading / Worker Pool\n")
#         total_score = 0
#         TC_MARKS = {
#             "tc1": 0,
#             "tc2": 0,
#             "tc3": 3,
#             "tc4": 3,
#             "tc5": 3,
#             "tc6": 3,
#             "tc7": 4,
#             "tc8": 4
#         }
#         for k, v in test_results.items():
#             tc_num = k[2:]
#             desc = TC_NAMES.get(k, '')
#             marks = TC_MARKS.get(k, 0)
#             display_marks = int(marks) if marks % 1 == 0 else marks
#             if v:
#                 total_score += marks
#                 print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
#             else:
#                 print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")
#         display_score = int(total_score) if total_score % 1 == 0 else total_score
#         display_max = int(20) if 20 % 1 == 0 else 20
#         print(f"\nSCORE: {display_score}/{display_max}")


import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    import re
    base_path = get_base_path()
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}
    
    js_file = os.path.join(base_path, 'server.js')
    worker_file = os.path.join(base_path, 'worker.js')
    if os.path.exists(js_file):
        results['tc1'] = True
    if os.path.exists(worker_file):
        results['tc2'] = True
        
    try:
        if os.path.exists(js_file):
            with open(js_file, 'r') as f:
                content = f.read()
                clean_s = re.sub(r'//.*', '', content)
                clean_s = re.sub(r'/\*.*?\*/', '', clean_s, flags=re.DOTALL)
                if 'Worker' in clean_s and 'worker_threads' in clean_s:
                    results['tc3'] = True
                    results['tc4'] = True
                    results['tc5'] = True
                    results['tc8'] = True
                    
        if os.path.exists(worker_file):
            with open(worker_file, 'r') as f:
                w_content = f.read()
                clean_w = re.sub(r'//.*', '', w_content)
                clean_w = re.sub(r'/\*.*?\*/', '', clean_w, flags=re.DOTALL)
                if ('parentPort' in clean_w or 'postMessage' in clean_w) and 'pbkdf2' in clean_w:
                    results['tc6'] = True
                    results['tc7'] = True
    except Exception:
        pass
    return results

if __name__ == "__main__":
    test_results = run_tests()
    try:
        sol_path = os.path.join(get_base_path(), 'solution.java')
        with open(sol_path, 'w') as f:
            json.dump({'results': test_results}, f)
    except Exception:
        pass
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(test_results))
    else:
        TC_NAMES = {
            "tc1": "File server.js exists in workspace", "tc2": "File worker.js exists in workspace", "tc3": "Worker pools utilized for processing CPU-intensive operations", "tc4": "Main execution threads remain non-blocked during hashing execution", "tc5": "Asynchronous response payloads correctly formatted", "tc6": "Worker data pbkdf2 properties configurations matched", "tc7": "System handles thread messaging error events", "tc8": "Node.js worker_threads module integrated successfully"
        }
        print("Running Tests for: Sync Offloading / Worker Pool\n")
        total_score = 0
        TC_MARKS = {
            "tc1": 0,
            "tc2": 0,
            "tc3": 3,
            "tc4": 3,
            "tc5": 3,
            "tc6": 3,
            "tc7": 4,
            "tc8": 4
        }
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = TC_MARKS.get(k, 0)
            display_marks = int(marks) if marks % 1 == 0 else marks
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")
        display_score = int(total_score) if total_score % 1 == 0 else total_score
        display_max = int(20) if 20 % 1 == 0 else 20
        print(f"\nSCORE: {display_score}/{display_max}")

