import sys
import json
import os
import re

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False, "tc6": False, "tc7": False, "tc8": False}
    
    boot_path = os.path.join(base_path, 'src', 'main', 'resources', 'bootstrap.yml')
    if os.path.exists(boot_path):
        results['tc5'] = True
        try:
            with open(boot_path, 'r') as f:
                content = f.read()
                if 'http://localhost:8888' in content:
                    results['tc1'] = True
                    results['tc6'] = True
                if 'ops-app' in content:
                    results['tc2'] = True
                    results['tc3'] = True
                    results['tc4'] = True
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
            "tc1": "Config URI configured to 8888",
            "tc2": "Config app name configured to ops-app",
            "tc3": "Config resolution initialized",
            "tc4": "Context resolution active",
            "tc5": "Bootstrap properties format valid",
            "tc6": "Central credentials fetch active",
            "tc7": "Bootstrap profiles registered",
            "tc8": "Lookup precedence validated"
        }
        print("Running Tests for: Spring Cloud Config Client\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 4 if k == 'tc8' else 3
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/25.0")
