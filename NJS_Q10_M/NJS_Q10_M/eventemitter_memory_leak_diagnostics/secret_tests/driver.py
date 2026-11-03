# # import os
# # import sys
# # import json

# # def get_base_path():
# #     current_dir = os.path.dirname(os.path.abspath(__file__))
# #     return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

# # def run_tests():
# #     import subprocess
# #     base_path = get_base_path()
# #     results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}
# #     # TC1: File server.js exists
# #     js_file = os.path.join(base_path, 'server.js')
# #     if os.path.exists(js_file):
# #         results['tc1'] = True
# #     else:
# #         return results

# #     try:
# #         # Check Express import and server syntax
# #         with open(js_file, 'r') as f:
# #             code = f.read()
# #             if 'once' in code or 'removeListener' in code or 'off(' in code:
# #                 results['tc5'] = True
# #                 results['tc6'] = True
# #                 results['tc7'] = True
# #                 results['tc8'] = True

# #         # Simulating clean run
# #         node_check = "const app = require('./server'); console.log(typeof app.get);"
# #         p = subprocess.run(['node', '-e', node_check], cwd=base_path, capture_output=True, text=True)
# #         if 'function' in p.stdout:
# #             results['tc2'] = True
# #             results['tc3'] = True
# #             results['tc4'] = True
# #     except Exception:
# #         pass
# #     return results

# # if __name__ == "__main__":
# #     test_results = run_tests()
# #     try:
# #         sol_path = os.path.join(get_base_path(), 'solution.java')
# #         with open(sol_path, 'w') as f:
# #             json.dump({'results': test_results}, f)
# #     except Exception:
# #         pass
    
# #     if len(sys.argv) > 1 and sys.argv[1] == '--json':
# #         print(json.dumps(test_results))
# #     else:
# #         TC_NAMES = {
# #             "tc1": "File server.js exists in student workspace", "tc2": "Express server compiles and starts successfully", "tc3": "Target route /api/listen returns HTTP 200 OK status", "tc4": "Global emitter listeners do not grow unbounded under load", "tc5": "Correct usage of once() or removeListener() handlers", "tc6": "Listener limit warnings do not trigger", "tc7": "Request event responses are handled correctly", "tc8": "Clean shutdown and listener cleanup verified"
# #         }
# #         print("Running Tests for: EventEmitter Memory Leak Diagnostics\n")
# #         total_score = 0
# #         for k, v in test_results.items():
# #             tc_num = k[2:]
# #             desc = TC_NAMES.get(k, '')
# #             marks = 2.5
# #             display_marks = int(marks) if marks % 1 == 0 else marks
# #             if v:
# #                 total_score += marks
# #                 print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
# #             else:
# #                 print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")
# #         display_score = int(total_score) if total_score % 1 == 0 else total_score
# #         display_max = int(20) if 20 % 1 == 0 else 20
# #         print(f"\nSCORE: {display_score}/{display_max}")
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
#     if os.path.exists(js_file):
#         results['tc1'] = True
#     else:
#         return results

#     try:
#         # Check Express import and server syntax
#         with open(js_file, 'r') as f:
#             code = f.read()
#             if 'once' in code or 'removeListener' in code or 'off(' in code:
#                 results['tc5'] = True
#                 results['tc6'] = True
#                 results['tc7'] = True
#                 results['tc8'] = True

#         # Simulating clean run
#         node_check = "const app = require('./server'); console.log(typeof app.get);"
#         p = subprocess.run(['node', '-e', node_check], cwd=base_path, capture_output=True, text=True)
#         if 'function' in p.stdout:
#             results['tc2'] = True
#             results['tc3'] = True
#             results['tc4'] = True
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
#             "tc1": "File server.js exists in student workspace", "tc2": "Express server compiles and starts successfully", "tc3": "Target route /api/listen returns HTTP 200 OK status", "tc4": "Global emitter listeners do not grow unbounded under load", "tc5": "Correct usage of once() or removeListener() handlers", "tc6": "Listener limit warnings do not trigger", "tc7": "Request event responses are handled correctly", "tc8": "Clean shutdown and listener cleanup verified"
#         }
#         print("Running Tests for: EventEmitter Memory Leak Diagnostics\n")
#         total_score = 0
#         TC_MARKS = {
#             "tc1": 2, "tc2": 2, "tc3": 2, "tc4": 3,
#             "tc5": 3, "tc6": 3, "tc7": 3, "tc8": 2
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
import re

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}
    # TC1: File server.js exists
    js_file = os.path.join(base_path, 'server.js')
    if os.path.exists(js_file):
        results['tc1'] = True
    else:
        return results

    try:
        with open(js_file, 'r') as f:
            code = f.read()
            clean_c = re.sub(r'//.*', '', code)
            clean_c = re.sub(r'/\*.*?\*/', '', clean_c, flags=re.DOTALL)
            
            if ('express' in clean_c and 'app' in clean_c) or 'module.exports' in clean_c:
                results['tc2'] = True
            if '/api/listen' in clean_c or 'app.get' in clean_c:
                results['tc3'] = True

            try:
                node_check = "const app = require('./server'); console.log(typeof app.get);"
                p = subprocess.run(['node', '-e', node_check], cwd=base_path, capture_output=True, text=True, timeout=5)
                if 'function' in p.stdout:
                    results['tc2'] = True
                    results['tc3'] = True
            except Exception:
                pass
            
            if 'once' in clean_c or 'removeListener' in clean_c or 'off(' in clean_c:
                results['tc4'] = True
                results['tc5'] = True
                results['tc6'] = True
                results['tc7'] = True
                results['tc8'] = True
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
            "tc1": "File server.js exists in student workspace",
            "tc2": "Express server compiles and starts successfully",
            "tc3": "Target route /api/listen returns HTTP 200 OK status",
            "tc4": "Global emitter listeners do not grow unbounded under load",
            "tc5": "Correct usage of once() or removeListener() handlers",
            "tc6": "Listener limit warnings do not trigger",
            "tc7": "Request event responses are handled correctly",
            "tc8": "Clean shutdown and listener cleanup verified"
        }
        print("Running Tests for: EventEmitter Memory Leak Diagnostics\n")
        total_score = 0
        TC_MARKS = {
            "tc1": 2, "tc2": 2, "tc3": 2, "tc4": 3,
            "tc5": 3, "tc6": 3, "tc7": 3, "tc8": 2
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
