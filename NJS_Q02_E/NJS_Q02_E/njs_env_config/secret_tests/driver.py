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
#     # TC1: File config.js exists
#     js_file = os.path.join(base_path, 'config.js')
#     if os.path.exists(js_file):
#         results['tc1'] = True
        
#     try:
#         process = subprocess.run(
#             ['node', 'config.js'],
#             cwd=base_path,
#             capture_output=True,
#             text=True,
#             timeout=10
#         )
#         report_path = os.path.join(base_path, 'config_report.json')
#         if os.path.exists(report_path):
#             with open(report_path, 'r') as f:
#                 config_data = json.load(f)
#                 if 'port' in config_data and 'env' in config_data:
#                     results['tc2'] = True
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
#             "tc1": "File config.js exists and runs successfully", "tc2": "JSON report config_report.json is correctly generated"
#         }
#         print("Running Tests for: Node.js Environment Configuration\n")
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
    base_path = get_base_path()
    results = {'tc1': False, 'tc2': False}
    
    report_path = os.path.join(base_path, 'config_report.json')
    if os.path.exists(report_path):
        try:
            os.remove(report_path)
        except Exception:
            pass

    js_file = os.path.join(base_path, 'config.js')
    if os.path.exists(js_file):
        try:
            process = subprocess.run(
                ['node', 'config.js'],
                cwd=base_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if process.returncode == 0:
                results['tc1'] = True
        except Exception:
            pass
            
    if os.path.exists(report_path):
        try:
            with open(report_path, 'r') as f:
                config_data = json.load(f)
                if 'port' in config_data and ('env' in config_data or 'NODE_ENV' in config_data or 'environment' in config_data):
                    results['tc2'] = True
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
            "tc1": "File config.js exists and runs successfully", "tc2": "JSON report config_report.json is correctly generated"
        }
        print("Running Tests for: Node.js Environment Configuration\n")
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

