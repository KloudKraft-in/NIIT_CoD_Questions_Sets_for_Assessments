import sys
import json
import os

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False}
    
    summary_path = os.path.join(base_path, 'log_summary.json')
    if os.path.exists(summary_path):
        try:
            with open(summary_path, 'r') as f:
                data = json.load(f)
                results['tc1'] = True
                
                npe = int(data.get('NullPointerException', 0))
                cnf = int(data.get('ClassNotFoundException', 0))
                bce = int(data.get('BeanCreationException', 0))
                
                if npe == 2:
                    results['tc2'] = True
                if cnf == 1:
                    results['tc3'] = True
                if bce == 1:
                    results['tc4'] = True
                    
                if results['tc2'] and results['tc3'] and results['tc4']:
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
            "tc1": "log_summary.json exists and is valid JSON",
            "tc2": "NullPointerException count is correct",
            "tc3": "ClassNotFoundException count is correct",
            "tc4": "BeanCreationException count is correct",
            "tc5": "All exception frequencies are correct"
        }
        print("Running Tests for: Common Java Log Signatures Analysis\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if v:
                total_score += 2
                print(f"PASS TC{tc_num} [{desc}] (2/2)")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/2)")
        print(f"\nSCORE: {total_score}/10.0")
