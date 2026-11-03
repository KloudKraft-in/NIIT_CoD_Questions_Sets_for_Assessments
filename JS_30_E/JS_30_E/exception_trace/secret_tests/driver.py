import sys
import json
import os

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {"tc1": False, "tc2": False, "tc3": False}
    
    txt_path = os.path.join(base_path, 'exception.txt')
    if os.path.exists(txt_path):
        results['tc1'] = True
        try:
            with open(txt_path, 'r') as f:
                content = f.read().strip()
                
            if len(content) > 0 and 'Exception' in content:
                results['tc2'] = True
                
            if content == 'NullPointerException':
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
            "tc1": "exception.txt exists",
            "tc2": "exception format matches",
            "tc3": "exception set to NullPointerException"
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
