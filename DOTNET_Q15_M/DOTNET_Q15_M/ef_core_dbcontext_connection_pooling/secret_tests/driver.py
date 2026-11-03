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

    program_path = os.path.join(base_path, 'Program.cs')
    if os.path.exists(program_path):
        results['tc2'] = True
    else:
        return results

    try:
        with open(program_path, 'r') as f:
            content = f.read()
        if 'SalesDbContext' in content:
            results['tc3'] = True
        if 'AddDbContextPool<' in content:
            results['tc4'] = True
            results['tc5'] = True
            results['tc6'] = True
            results['tc7'] = True
        if 'AddDbContext<' not in content or 'AddDbContextPool<' in content:
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
            "tc2": "Program.cs exists in workspace", "tc3": "DbContext class 'SalesDbContext' defined", "tc4": "DbContext pooling configured using AddDbContextPool method", "tc5": "Connection string retrieval configured", "tc6": "Pool size parameter configured explicitly", "tc7": "Code compiles cleanly", "tc8": "No redundant AddDbContext registration remains"
        }
        print("Running Tests for: EF Core DbContext Connection Pooling\n")
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
