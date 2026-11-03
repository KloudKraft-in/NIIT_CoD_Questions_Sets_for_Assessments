import sys
import json
import os
import re

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {"tc1": False, "tc2": False, "tc3": False}
    
    props_path = os.path.join(base_path, 'src', 'main', 'resources', 'application.properties')
    if os.path.exists(props_path):
        results['tc1'] = True
        try:
            with open(props_path, 'r') as f:
                content = f.read()
                if re.search(r'management\.endpoints\.web\.exposure\.include\s*=\s*(health|\*)', content):
                    results['tc2'] = True
                    results['tc3'] = True
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
            "tc1": "application.properties exists",
            "tc2": "Exposure include contains health",
            "tc3": "Exposure format correctly parsed"
        }
        print("Running Tests for: Basic Spring Boot Actuator Health Check\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 3 if k in ['tc1', 'tc3'] else 4
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/10.0")
