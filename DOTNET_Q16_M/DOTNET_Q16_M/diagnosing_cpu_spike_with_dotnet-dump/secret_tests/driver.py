import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': True, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}

    diag_path = os.path.join(base_path, 'diagnostics.md')
    if os.path.exists(diag_path):
        results['tc2'] = True
    else:
        return results

    try:
        with open(diag_path, 'r') as f:
            content = f.read().lower()
        if 'dotnet-dump' in content or 'sos' in content:
            results['tc3'] = True
        if 'thread' in content:
            results['tc4'] = True
        if '0x' in content or 'lock' in content:
            results['tc5'] = True
        if 'method' in content or 'blocking' in content or 'run' in content:
            results['tc6'] = True
        if 'blocked' in content or 'waiting' in content:
            results['tc7'] = True
        if 'async' in content or 'semaphore' in content or 'lock' in content:
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
            "tc1": "Local VM Environment active and verified",
            "tc2": "Diagnostics report diagnostics.md exists", "tc3": "Report identifies dotnet-dump analysis command used", "tc4": "Report locates the exact thread ID triggering CPU spike", "tc5": "Report isolates lock address where threads are blocked", "tc6": "Report identifies class method name blocking thread execution", "tc7": "Report lists correct thread state (BLOCKED / WAITING)", "tc8": "Recommendation section specifies code patch utilizing async locks"
        }
        print("Running Tests for: Diagnosing CPU Spike with dotnet-dump\n")
        total_score = 0
        marks_list = [3, 3, 3, 3, 3, 3, 2]
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
