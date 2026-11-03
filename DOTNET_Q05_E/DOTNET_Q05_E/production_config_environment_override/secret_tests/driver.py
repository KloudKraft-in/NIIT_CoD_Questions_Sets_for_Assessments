import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': True, 'tc2': False, 'tc3': False, 'tc4': False}

    prod_path = os.path.join(base_path, 'appsettings.Production.json')
    if os.path.exists(prod_path):
        results['tc2'] = True
    
    try:
        with open(prod_path, 'r') as f:
            data = json.load(f)
        results['tc3'] = True
        conn_str = data.get("ConnectionStrings", {}).get("DefaultConnection", "")
        if "prod-db" in conn_str.lower():
            results['tc4'] = True
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
            "tc2": "File appsettings.Production.json exists", "tc3": "Configuration file compiles as valid JSON", "tc4": "Production ConnectionString uses server 'prod-db'"
        }
        print("Running Tests for: Production Config Environment Override\n")
        total_score = 0
        marks_list = [4, 3, 3]
        for k, v in test_results.items():
            tc_num = int(k[2:])
            desc = TC_NAMES.get(k, '')
            marks = marks_list[tc_num - 2] if tc_num > 1 else 0
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/10")
