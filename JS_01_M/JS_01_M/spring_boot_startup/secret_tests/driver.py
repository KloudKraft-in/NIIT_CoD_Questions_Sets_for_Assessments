# import sys
# import json
# import os
# import subprocess
# import urllib.request
# import urllib.error
# import socket
# import re

# def get_base_path():
#     # Attempt to get the workspace directory
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

#     # TC1: Compile codebase
#     try:
#         process = subprocess.run(
#             ['mvn', 'clean', 'compile'],
#             cwd=base_path,
#             capture_output=True,
#             text=True
#         )
#         if process.returncode == 0:
#             results['tc1'] = True
#     except Exception:
#         pass

#     # TC2: Check for Stereotype annotation in UserService
#     try:
#         user_service_path = os.path.join(base_path, 'src/main/java/com/kloudlabs/app/service/UserService.java')
#         with open(user_service_path, 'r') as f:
#             content = f.read()
#             if '@Service' in content or '@Component' in content:
#                 results['tc2'] = True
#     except Exception:
#         pass

#     # TC3: Check application.properties for port 8081
#     try:
#         props_path = os.path.join(base_path, 'src/main/resources/application.properties')
#         with open(props_path, 'r') as f:
#             content = f.read()
#             if re.search(r'server\.port\s*=\s*8081', content):
#                 results['tc3'] = True
#     except Exception:
#         pass

#     # TC4: Check if application is listening on port 8081
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(2)
#         result = sock.connect_ex(('127.0.0.1', 8081))
#         if result == 0:
#             results['tc4'] = True
#         sock.close()
#     except Exception:
#         pass

#     # TC5: Check actuator health endpoint
#     try:
#         req = urllib.request.Request('http://localhost:8081/actuator/health')
#         with urllib.request.urlopen(req, timeout=3) as response:
#             if response.status == 200:
#                 data = json.loads(response.read().decode())
#                 if data.get('status') == 'UP':
#                     results['tc5'] = True
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
#             "tc1": "Compile codebase",
#             "tc2": "Stereotype annotation in UserService",
#             "tc3": "application.properties server port",
#             "tc4": "Application listening on port 8081",
#             "tc5": "Actuator health endpoint"
#         }
#         print("Running Tests for: Spring Boot Startup Troubleshooting\n")
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
import urllib.request
import urllib.error
import socket
import re

def get_base_path():
    # Attempt to get the workspace directory
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

    # TC1: Compile codebase
    try:
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
                for sub_args in ['clean compile', 'compile']:
                    full_cmd = f'"{mvn_bin}" {sub_args}' if os.path.isabs(mvn_bin) else f'{mvn_bin} {sub_args}'
                    try:
                        proc = subprocess.run(
                            full_cmd,
                            cwd=base_path,
                            capture_output=True,
                            text=True,
                            shell=True
                        )
                        if proc.returncode == 0:
                            results['tc1'] = True
                            break
                    except Exception:
                        pass
                    try:
                        cmd_list = [mvn_bin] + sub_args.split()
                        proc = subprocess.run(
                            cmd_list,
                            cwd=base_path,
                            capture_output=True,
                            text=True,
                            shell=False
                        )
                        if proc.returncode == 0:
                            results['tc1'] = True
                            break
                    except Exception:
                        pass
                if results['tc1']:
                    break
        else:
            process = subprocess.run(
                ['mvn', 'clean', 'compile'],
                cwd=base_path,
                capture_output=True,
                text=True
            )
            if process.returncode == 0:
                results['tc1'] = True
    except Exception:
        pass

    # TC2: Check for Stereotype annotation in UserService
    try:
        user_service_path = os.path.join(base_path, 'src/main/java/com/kloudlabs/app/service/UserService.java')
        with open(user_service_path, 'r') as f:
            content = f.read()
            if '@Service' in content or '@Component' in content:
                results['tc2'] = True
    except Exception:
        pass

    # TC3: Check application.properties for port 8081
    try:
        props_path = os.path.join(base_path, 'src/main/resources/application.properties')
        with open(props_path, 'r') as f:
            content = f.read()
            if re.search(r'server\.port\s*=\s*8081', content):
                results['tc3'] = True
    except Exception:
        pass

    # TC4: Check if application is listening on port 8081
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', 8081))
        if result == 0:
            results['tc4'] = True
        sock.close()
    except Exception:
        pass

    # TC5: Check actuator health endpoint
    try:
        req = urllib.request.Request('http://localhost:8081/actuator/health')
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                if data.get('status') == 'UP':
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
            "tc1": "Compile codebase",
            "tc2": "Stereotype annotation in UserService",
            "tc3": "application.properties server port",
            "tc4": "Application listening on port 8081",
            "tc5": "Actuator health endpoint"
        }
        print("Running Tests for: Spring Boot Startup Troubleshooting\n")
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

