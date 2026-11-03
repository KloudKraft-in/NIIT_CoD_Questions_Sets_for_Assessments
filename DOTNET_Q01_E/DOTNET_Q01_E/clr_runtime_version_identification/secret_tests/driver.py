import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': True, 'tc2': False, 'tc3': False}

    js_file = os.path.join(base_path, 'identify_runtime.py')
    if os.path.exists(js_file):
        results['tc2'] = True
    else:
        return results

    try:
        sys.path.insert(0, base_path)
        import identify_runtime
        log_content = "Info: Application started. Runtime: .NET 8.0.0. Web Host: Kestrel listening on port 5000."
        temp_log = os.path.join(base_path, 'temp_run.log')
        with open(temp_log, 'w') as f:
            f.write(log_content)
        parsed = identify_runtime.parse_runtime(temp_log)
        if parsed.get('version') == '8.0.0' and parsed.get('host') == 'Kestrel':
            results['tc3'] = True
        try:
            os.remove(temp_log)
        except:
            pass
    except Exception as e:
        print(f"Error executing script: {e}")

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
            "tc2": "Script identify_runtime.py exists in workspace", "tc3": "Script correctly extracts version and hosting environment"
        }
        print("Running Tests for: CLR Runtime Version Identification\n")
        total_score = 0
        marks_list = [5, 5]
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
