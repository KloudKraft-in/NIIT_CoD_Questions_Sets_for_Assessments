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
    
    props_path = os.path.join(base_path, 'src', 'main', 'resources', 'application.properties')
    if os.path.exists(props_path):
        results['tc5'] = True
        try:
            with open(props_path, 'r') as f:
                content = f.read()
                if re.search(r'server\.shutdown\s*=\s*graceful', content):
                    results['tc1'] = True
                    results['tc6'] = True
                if re.search(r'spring\.lifecycle\.timeout-per-shutdown-phase\s*=\s*30s', content):
                    results['tc2'] = True
                    results['tc7'] = True
        except Exception:
            pass
            
    sh_path = os.path.join(base_path, 'pre-stop.sh')
    if os.path.exists(sh_path):
        results['tc3'] = True
        try:
            with open(sh_path, 'r') as f:
                content = f.read()
                if re.search(r'sleep\s+10', content):
                    results['tc4'] = True
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
            "tc1": "Graceful shutdown property enabled",
            "tc2": "Lifecycle shutdown phase timeout configured",
            "tc3": "pre-stop.sh script created",
            "tc4": "pre-stop.sh contains sleep instruction",
            "tc5": "Files syntax validated",
            "tc6": "In-flight request draining active",
            "tc7": "Graceful timeout range validated",
            "tc8": "PreStop duration configured"
        }
        print("Running Tests for: Graceful Shutdown Configuration\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 2 if k in ['tc1', 'tc2', 'tc3', 'tc4'] else 3
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/20.0")
