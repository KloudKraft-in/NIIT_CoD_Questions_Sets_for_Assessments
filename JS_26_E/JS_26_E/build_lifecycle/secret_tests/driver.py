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
    
    pom_path = os.path.join(base_path, 'pom.xml')
    if os.path.exists(pom_path):
        results['tc1'] = True
        try:
            with open(pom_path, 'r') as f:
                content = f.read()
                
            if 'project.build.sourceEncoding' in content:
                results['tc2'] = True
                
            if re.search(r'<project\.build\.sourceEncoding>\s*UTF-8\s*</project\.build\.sourceEncoding>', content):
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
            "tc1": "pom.xml exists",
            "tc2": "project.build.sourceEncoding defined",
            "tc3": "encoding property set to UTF-8"
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
