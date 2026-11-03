import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': False, 'tc2': False}
    # TC1: File index.js exists
    js_file = os.path.join(base_path, 'index.js')
    if os.path.exists(js_file):
        results['tc1'] = True
    else:
        return results

    # Run the node process
    try:
        process = subprocess.run(
            ['node', 'index.js'],
            cwd=base_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if process.returncode == 0:
            # Parse output sequence
            output_lines = [line.strip() for line in process.stdout.splitlines() if line.strip()]
            if (len(output_lines) >= 6 and 
                output_lines[0] == "start" and 
                output_lines[1] == "end" and 
                output_lines[2] == "nextTick" and 
                output_lines[3] == "promise" and 
                "timeout" in output_lines[4:] and 
                "immediate" in output_lines[4:]):
                results['tc2'] = True
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
            "tc1": "File index.js exists and compiles cleanly", "tc2": "Execution output order matches Event Loop phase priorities"
        }
        print("Running Tests for: Event Loop Phase Execution Order\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            marks = 5
            display_marks = int(marks) if marks % 1 == 0 else marks
            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")
        display_score = int(total_score) if total_score % 1 == 0 else total_score
        display_max = int(10) if 10 % 1 == 0 else 10
        print(f"\nSCORE: {display_score}/{display_max}")
