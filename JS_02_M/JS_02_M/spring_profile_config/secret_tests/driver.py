# import sys
# import json
# import os
# import subprocess
# import stat

# def get_base_path():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

# def run_tests():
#     base_path = get_base_path()
#     results = {
#         "tc1": False,
#         "tc2": False,
#         "tc3": False,
#         "tc4": False,
#         "tc5": False
#     }

#     script_path = os.path.join(base_path, 'extract.sh')
#     output_path = os.path.join(base_path, 'output.txt')

#     # TC1: Check if script exists, has execution permissions, and runs
#     try:
#         if os.path.exists(script_path):
#             st = os.stat(script_path)
#             if bool(st.st_mode & stat.S_IXUSR):
#                 process = subprocess.run(['./extract.sh'], cwd=base_path, capture_output=True, timeout=5)
#                 if process.returncode == 0:
#                     results['tc1'] = True
#     except Exception:
#         pass

#     # Read output.txt for remaining TCs
#     try:
#         if os.path.exists(output_path):
#             results['tc2'] = True
#             with open(output_path, 'r') as f:
#                 content = f.read().strip()
            
#             if content:
#                 results['tc3'] = True
                
#             if 'prod_ultra_secure_pw_987!@#' in content:
#                 results['tc4'] = True
                
#             if 'dev_super_secret_pw_123' not in content and 'default_password' not in content:
#                 results['tc5'] = True
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
#             "tc1": "Check if extract.sh exists and runs",
#             "tc2": "Output file generated successfully",
#             "tc3": "Configuration content loaded",
#             "tc4": "Production profile active",
#             "tc5": "Development profile inactive"
#         }
#         print("Running Tests for: Spring Profile Configuration\n")
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
import subprocess
import stat

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False
    }

    script_path = os.path.join(base_path, 'extract.sh')
    output_path = os.path.join(base_path, 'output.txt')

    # TC1: Check if script exists, has execution permissions, and runs
    try:
        if os.path.exists(script_path):
            st = os.stat(script_path)
            has_permission = True if os.name == 'nt' else bool(st.st_mode & stat.S_IXUSR)
            if has_permission:
                process = None
                if os.name == 'nt':
                    bash_candidates = [
                        r'C:\Program Files\Git\bin\bash.exe',
                        r'C:\Program Files\Git\bin\sh.exe',
                        r'C:\Program Files (x86)\Git\bin\bash.exe',
                        r'C:\Program Files (x86)\Git\bin\sh.exe',
                        'bash',
                        'sh'
                    ]
                    for bash_bin in bash_candidates:
                        try:
                            process = subprocess.run(
                                [bash_bin, 'extract.sh'],
                                cwd=base_path,
                                capture_output=True,
                                timeout=5,
                                shell=True
                            )
                            if process.returncode == 0:
                                break
                        except Exception:
                            continue
                else:
                    try:
                        process = subprocess.run(['./extract.sh'], cwd=base_path, capture_output=True, timeout=5)
                    except Exception:
                        try:
                            process = subprocess.run(['bash', 'extract.sh'], cwd=base_path, capture_output=True, timeout=5)
                        except Exception:
                            pass

                if process and process.returncode == 0:
                    results['tc1'] = True
    except Exception:
        pass

    # Read output.txt for remaining TCs
    try:
        if os.path.exists(output_path):
            results['tc2'] = True
            with open(output_path, 'r') as f:
                content = f.read().strip()
            
            if content:
                results['tc3'] = True
                
            if 'prod_ultra_secure_pw_987!@#' in content:
                results['tc4'] = True
                
            if 'dev_super_secret_pw_123' not in content and 'default_password' not in content:
                results['tc5'] = True
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
            "tc1": "Check if extract.sh exists and runs",
            "tc2": "Output file generated successfully",
            "tc3": "Configuration content loaded",
            "tc4": "Production profile active",
            "tc5": "Development profile inactive"
        }
        print("Running Tests for: Spring Profile Configuration\n")
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
