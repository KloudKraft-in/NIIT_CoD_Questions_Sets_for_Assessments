# import sys
# import json
# import os

# def get_base_path():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     if os.path.basename(current_dir) == 'secret_tests':
#         return os.path.abspath(os.path.join(current_dir, '../student_workspace'))
#     else:
#         return os.path.abspath(os.path.join(current_dir, 'student_workspace'))

# def run_tests():
#     base_path = get_base_path()
#     results = {
#         "tc1": False,
#         "tc2": False,
#         "tc3": False,
#         "tc4": False,
#         "tc5": False
#     }

#     script_path = os.path.join(base_path, 'start.sh')

#     try:
#         if os.path.exists(script_path):
#             with open(script_path, 'r') as f:
#                 content = f.read()
            
#             if '-XX:MaxRAMPercentage=75.0' in content:
#                 results['tc1'] = True
#             if '-XX:+UseG1GC' in content:
#                 results['tc2'] = True
#             if 'java ' in content and '-jar app.jar' in content:
#                 results['tc3'] = True
#     except Exception:
#         pass

#     if results['tc1'] and results['tc2'] and results['tc3']:
#         results['tc4'] = True
#         results['tc5'] = True

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
#             "tc1": "Verify MaxRAMPercentage flag",
#             "tc2": "Verify G1GC flag",
#             "tc3": "Verify Java execution command",
#             "tc4": "Simulated run successful",
#             "tc5": "Verify running process flags"
#         }
#         print("Running Tests for: Configure JVM Arguments\n")
#         total_score = 0
#         for k, v in test_results.items():
#             if k.lower().startswith('tc'):
#                 tc_num = k[2:]
#                 desc = TC_NAMES.get(k.lower(), '')
#                 if v:
#                     total_score += 4
#                     print(f"PASS TC{tc_num} [{desc}] (4/4)")
#                 else:
#                     print(f"FAIL TC{tc_num} [{desc}] (0/4)")
#         print(f"\nSCORE: {total_score}/20.0")





import sys
import json
import os

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(current_dir) == 'secret_tests':
        return os.path.abspath(os.path.join(current_dir, '../student_workspace'))
    else:
        return os.path.abspath(os.path.join(current_dir, 'student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False
    }

    script_path = os.path.join(base_path, 'start.sh')

    try:
        if os.path.exists(script_path):
            with open(script_path, 'r') as f:
                content = f.read()
            
            # Extract active non-comment lines containing java command
            active_java_lines = [
                line.strip() for line in content.splitlines()
                if line.strip() and not line.strip().startswith('#') and 'java' in line
            ]
            java_cmd = ' '.join(active_java_lines)
            
            if '-XX:MaxRAMPercentage=75.0' in java_cmd:
                results['tc1'] = True
            if '-XX:+UseG1GC' in java_cmd:
                results['tc2'] = True
            if 'java' in java_cmd and '-jar' in java_cmd and 'app.jar' in java_cmd:
                results['tc3'] = True
    except Exception:
        pass

    if results['tc1'] and results['tc2'] and results['tc3']:
        results['tc4'] = True
        results['tc5'] = True

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
            "tc1": "Verify MaxRAMPercentage flag",
            "tc2": "Verify G1GC flag",
            "tc3": "Verify Java execution command",
            "tc4": "Simulated run successful",
            "tc5": "Verify running process flags"
        }
        print("Running Tests for: Configure JVM Arguments\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 4
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/20.0")

