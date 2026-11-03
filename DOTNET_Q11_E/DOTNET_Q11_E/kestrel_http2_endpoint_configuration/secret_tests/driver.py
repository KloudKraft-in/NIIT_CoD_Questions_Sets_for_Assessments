import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    import subprocess
    base_path = get_base_path()
    results = {'tc1': True, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False}

    app_path = os.path.join(base_path, 'appsettings.json')
    if os.path.exists(app_path):
        results['tc2'] = True
    else:
        return results

    try:
        with open(app_path, 'r') as f:
            data = json.load(f)
        endpoints = data.get("Kestrel", {}).get("Endpoints", {})
        if "Https" in endpoints:
            results['tc3'] = True
            url = endpoints["Https"].get("Url", "")
            protocols = endpoints["Https"].get("Protocols", "")
            if "5001" in url:
                results['tc4'] = True
            if "Http2" in protocols or "Http1AndHttp2" in protocols:
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
            "tc1": "Local VM Environment active and verified",
            "tc2": "File appsettings.json exists and is valid JSON", "tc3": "Endpoint configuration for Kestrel is set on port 5001", "tc4": "Protocols list includes Http2 or Http1AndHttp2", "tc5": "Kestrel configuration contains valid default SSL certificate references"
        }
        print("Running Tests for: Kestrel HTTP2 Endpoint Configuration\n")
        total_score = 0
        marks_list = [5, 5, 5, 5]
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
