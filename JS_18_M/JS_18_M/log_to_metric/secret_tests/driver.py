import sys
import json
import os

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    base_path = get_base_path()
    results = {"tc1": False, "tc2": False, "tc3": False}
    
    pipeline_path = os.path.join(base_path, 'pipeline.json')
    if os.path.exists(pipeline_path):
        try:
            with open(pipeline_path, 'r') as f:
                data = json.load(f)
                results['tc1'] = True
                
                pat = data.get('pattern')
                m_name = data.get('metric_name')
                m_type = data.get('metric_type')
                
                if str(pat).strip() == 'HTTP 500':
                    results['tc2'] = True
                    
                if str(m_name).strip() == 'http_5xx_errors' and str(m_type).strip() == 'counter':
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
            "tc1": "pipeline.json exists and is valid JSON",
            "tc2": "pattern is set exactly to 'HTTP 500'",
            "tc3": "metric_name is 'http_5xx_errors' and metric_type is 'counter'"
        }
        print("Running Tests for: Log-to-Metric Error Pipeline\n")
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
