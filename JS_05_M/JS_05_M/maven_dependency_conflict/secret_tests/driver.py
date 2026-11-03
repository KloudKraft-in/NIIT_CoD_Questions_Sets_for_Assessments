# import sys
# import json
# import os
# import subprocess
# import re

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

#     pom_path = os.path.join(base_path, 'pom.xml')
    
#     try:
#         with open(pom_path, 'r') as f:
#             content = f.read()
            
#         # TC1: POM has been modified to include exclusion
#         if '<exclusion>' in content or '<exclusions>' in content:
#             results['tc1'] = True
            
#         # TC2: Exclusion is for guava
#         if re.search(r'<exclusion>[\s\S]*?<groupId>\s*com\.google\.guava\s*</groupId>[\s\S]*?<artifactId>\s*guava\s*</artifactId>[\s\S]*?</exclusion>', content):
#             results['tc2'] = True
#     except Exception:
#         pass

#     # TC3 & TC4: Maven tasks
#     try:
#         # Compile
#         compile_proc = subprocess.run(['mvn', 'clean', 'compile'], cwd=base_path, capture_output=True, text=True)
#         if compile_proc.returncode == 0:
#             results['tc4'] = True
            
#         # Dependency tree (check if old guava is excluded)
#         tree_proc = subprocess.run(['mvn', 'dependency:tree'], cwd=base_path, capture_output=True, text=True)
#         if tree_proc.returncode == 0:
#             # If guava is excluded from hadoop, the only guava should be the top-level 32.1.3
#             if 'guava:20' not in tree_proc.stdout and 'guava:27' not in tree_proc.stdout:
#                 results['tc3'] = True
#     except Exception:
#         pass

#     # TC5: Simulated run successful (If it compiles and no conflict, it passes)
#     if results['tc2'] and results['tc4']:
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
#             "tc1": "POM modified to include exclusion",
#             "tc2": "Exclusion targets Guava dependency",
#             "tc3": "Maven tasks execute successfully",
#             "tc4": "Dependency tree resolves correctly",
#             "tc5": "Simulated run successful"
#         }
#         print("Running Tests for: Maven Dependency Conflict\n")
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
import re

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_maven_cmd(cmd_args_str, base_path):
    if os.name == 'nt':
        mvn_execs = [
            r'C:\Program Files\Maven\apache-maven-3.9.16\bin\mvn.cmd',
        ]
        for env_var in ['MAVEN_HOME', 'M2_HOME']:
            val = os.environ.get(env_var)
            if val:
                mvn_execs.append(os.path.join(val, 'bin', 'mvn.cmd'))
        mvn_execs.extend([
            r'C:\Program Files\apache-maven-3.9.16\bin\mvn.cmd',
            r'C:\Program Files\Maven\bin\mvn.cmd',
            r'C:\Program Files\apache-maven\bin\mvn.cmd',
            r'C:\apache-maven-3.9.16\bin\mvn.cmd',
            r'C:\Maven\bin\mvn.cmd',
            'mvn.cmd',
            'mvn'
        ])

        cmds_to_try = []
        for ex in mvn_execs:
            if os.path.isabs(ex):
                if os.path.exists(ex) and ex not in cmds_to_try:
                    cmds_to_try.append(ex)
            elif ex not in cmds_to_try:
                cmds_to_try.append(ex)

        for mvn_bin in cmds_to_try:
            full_cmd = f'"{mvn_bin}" {cmd_args_str}' if os.path.isabs(mvn_bin) else f'{mvn_bin} {cmd_args_str}'
            try:
                proc = subprocess.run(
                    full_cmd,
                    cwd=base_path,
                    capture_output=True,
                    text=True,
                    shell=True
                )
                if proc.returncode == 0:
                    return proc
            except Exception:
                pass
            try:
                cmd_list = [mvn_bin] + cmd_args_str.split()
                proc = subprocess.run(
                    cmd_list,
                    cwd=base_path,
                    capture_output=True,
                    text=True,
                    shell=False
                )
                if proc.returncode == 0:
                    return proc
            except Exception:
                pass
        return None
    else:
        try:
            return subprocess.run(
                ['mvn'] + cmd_args_str.split(),
                cwd=base_path,
                capture_output=True,
                text=True
            )
        except Exception:
            return None

def run_tests():
    base_path = get_base_path()
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False
    }

    pom_path = os.path.join(base_path, 'pom.xml')
    
    try:
        with open(pom_path, 'r') as f:
            content = f.read()
            
        # TC1: POM has been modified to include exclusion
        if '<exclusion>' in content or '<exclusions>' in content:
            results['tc1'] = True
            
        # TC2: Exclusion is for guava
        if re.search(r'<exclusion>[\s\S]*?<groupId>\s*com\.google\.guava\s*</groupId>[\s\S]*?<artifactId>\s*guava\s*</artifactId>[\s\S]*?</exclusion>', content):
            results['tc2'] = True
    except Exception:
        pass

    # TC3 & TC4: Maven tasks
    try:
        # Compile
        compile_proc = run_maven_cmd('clean compile', base_path)
        if compile_proc and compile_proc.returncode == 0:
            results['tc4'] = True
            
        # Dependency tree (check if old guava is excluded)
        tree_proc = run_maven_cmd('dependency:tree', base_path)
        if tree_proc and tree_proc.returncode == 0:
            # If guava is excluded from hadoop, the only guava should be the top-level 32.1.3
            if 'guava:20' not in tree_proc.stdout and 'guava:27' not in tree_proc.stdout:
                results['tc3'] = True
    except Exception:
        pass

    # TC5: Simulated run successful (If it compiles and no conflict, it passes)
    if results['tc2'] and results['tc4']:
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
            "tc1": "POM modified to include exclusion",
            "tc2": "Exclusion targets Guava dependency",
            "tc3": "Maven tasks execute successfully",
            "tc4": "Dependency tree resolves correctly",
            "tc5": "Simulated run successful"
        }
        print("Running Tests for: Maven Dependency Conflict\n")
        total_score = 0
        for k, v in test_results.items():
            if k.lower().startswith('tc'):
                tc_num = k[2:]
                desc = TC_NAMES.get(k.lower(), '')
                if v:
                    total_score += 4
                    print(f"PASS TC{tc_num} [{desc}] (4/4)")
                else:
                    print(f"FAIL TC{tc_num} [{desc}] (0/4)")
        print(f"\nSCORE: {total_score}/20.0")



