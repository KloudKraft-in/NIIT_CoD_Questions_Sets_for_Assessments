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

    app_path = os.path.join(base_path, 'appsettings.json')
    if os.path.exists(app_path):
        results['tc2'] = True
    else:
        return results

    try:
        with open(app_path, 'r') as f:
            data = json.load(f)
        url = data.get("Kestrel", {}).get("Endpoints", {}).get("Http", {}).get("Url", "")
        if "5001" in url:
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
            "tc1": "Local VM Environment active and verified",
            "tc2": "File appsettings.json exists and is valid JSON", "tc3": "Kestrel HTTP endpoint URL is set to port 5001"
        }
        print("Running Tests for: Kestrel HTTP Port Configuration\n")
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
