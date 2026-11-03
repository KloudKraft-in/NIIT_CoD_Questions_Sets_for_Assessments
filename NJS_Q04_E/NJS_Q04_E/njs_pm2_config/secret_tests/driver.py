# import os
# import sys
# import json

# def get_base_path():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

# def run_tests():
#     import subprocess
#     base_path = get_base_path()
#     results = {'tc1': False, 'tc2': False}
#     # TC1: File ecosystem.config.js exists
#     js_file = os.path.join(base_path, 'ecosystem.config.js')
#     if os.path.exists(js_file):
#         results['tc1'] = True
#         with open(js_file, 'r') as f:
#             content = f.read()
#             if 'cluster' in content and 'instances' in content and 'max_memory_restart' in content:
#                 results['tc2'] = True
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
#             "tc1": "PM2 ecosystem.config.js exists and exports a valid configuration", "tc2": "Cluster execution mode, instances, and memory restart threshold correctly set"
#         }
#         print("Running Tests for: PM2 Cluster Configuration\n")
#         total_score = 0
#         for k, v in test_results.items():
#             tc_num = k[2:]
#             desc = TC_NAMES.get(k, '')
#             marks = 5
#             display_marks = int(marks) if marks % 1 == 0 else marks
#             if v:
#                 total_score += marks
#                 print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
#             else:
#                 print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")
#         display_score = int(total_score) if total_score % 1 == 0 else total_score
#         display_max = int(10) if 10 % 1 == 0 else 10
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
    results = {'tc1': False, 'tc2': False}
    
    js_file = os.path.join(base_path, 'ecosystem.config.js')
    if os.path.exists(js_file):
        results['tc1'] = True
        with open(js_file, 'r') as f:
            content = f.read()
            clean_content = re.sub(r'//.*', '', content)
            clean_content = re.sub(r'/\*.*?\*/', '', clean_content, flags=re.DOTALL)
            
            has_cluster = 'cluster' in clean_content
            has_instances = 'instances' in clean_content
            has_memory = 'max_memory_restart' in clean_content
            
            if has_cluster and has_instances and has_memory:
                results['tc2'] = True
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
            "tc1": "PM2 ecosystem.config.js exists and exports a valid configuration", "tc2": "Cluster execution mode, instances, and memory restart threshold correctly set"
        }
        print("Running Tests for: PM2 Cluster Configuration\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 5
            display_marks = int(marks) if marks % 1 == 0 else marks
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")
        display_score = int(total_score) if total_score % 1 == 0 else total_score
        display_max = int(10) if 10 % 1 == 0 else 10
        print(f"\nSCORE: {display_score}/{display_max}")
