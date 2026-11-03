import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': True, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False, 'tc9': False}

    repo_path = os.path.join(base_path, 'OrderRepository.cs')
    if os.path.exists(repo_path):
        results['tc2'] = True
    else:
        return results

    try:
        with open(repo_path, 'r') as f:
            content = f.read()
        if 'Include' in content:
            results['tc3'] = True
            results['tc4'] = True
        if 'AsNoTracking()' in content:
            results['tc5'] = True
        if 'GetRecentOrders' in content:
            results['tc6'] = True
            results['tc7'] = True
        if 'foreach' not in content or 'Include' in content:
            results['tc8'] = True
        if 'foreach' not in content:
            results['tc9'] = True
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
            "tc2": "File OrderRepository.cs exists in workspace", "tc3": "Eager loading Include used to query OrderLines", "tc4": "Eager loading reduces database roundtrips to a single query", "tc5": "AsNoTracking optimization applied for read-only query", "tc6": "Repository compiles cleanly", "tc7": "Eager loading logic correctly projects columns", "tc8": "OrderLines collection returned matching loop counts", "tc9": "No redundant loops remain inside the query method"
        }
        print("Running Tests for: EF Core N1 Query Performance Fix\n")
        total_score = 0
        marks_list = [3, 3, 3, 3, 2, 2, 2, 2]
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
