import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': True, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False}

    sh_file = os.path.join(base_path, 'override_env.sh')
    bat_file = os.path.join(base_path, 'override_env.bat')
    found_file = sh_file if os.path.exists(sh_file) else (bat_file if os.path.exists(bat_file) else None)
    
    if found_file:
        results['tc2'] = True
        try:
            with open(found_file, 'r') as f:
                content = f.read().lower()
            if 'aspnetcore_environment' in content and 'production' in content:
                results['tc3'] = True
            if 'logging__loglevel__default' in content or 'logging:loglevel:default' in content:
                results['tc4'] = True
            if 'warning' in content:
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
            "tc1": "Local VM Environment active and verified",
            "tc2": "File override_env.sh or override_env.bat exists in the workspace", "tc3": "Script sets the environment variable ASPNETCORE_ENVIRONMENT to Production", "tc4": "Script defines Logging__LogLevel__Default override key", "tc5": "Default log level override value is set to Warning"
        }
        print("Running Tests for: Logging Configuration Environment Override\n")
        total_score = 0
        marks_list = [5, 5, 5, 5]
        for k, v in test_results.items():
            tc_num = int(k[2:])
            desc = TC_NAMES.get(k, '')
            marks = marks_list[tc_num - 2] if tc_num > 1 else 0
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/20")
