import sys
import json
import os

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {"tc1": False, "tc2": False, "tc3": False}
    
    yml_path = os.path.join(base_path, 'application.yml')
    if os.path.exists(yml_path):
        try:
            with open(yml_path, 'r') as f:
                content = f.read()
                
            results['tc1'] = True
            # Simple line parsing to avoid yaml dependency problems in student env
            if 'server:' in content:
                results['tc2'] = True
                
            lines = [l.strip() for l in content.split('\n')]
            if 'port: 8080' in lines or 'port: "8080"' in lines:
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
            "tc1": "application.yml exists",
            "tc2": "server key is present",
            "tc3": "port set to 8080"
        }
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 3 if k in ['tc1', 'tc2'] else 4
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/10.0")
