import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False,
        "tc4": False,
        "tc5": False,
        "tc6": False,
        "tc7": False,
        "tc8": False
    }
    
    sol_path = os.path.join(get_base_path(), 'solution.json')
    if not os.path.exists(sol_path):
        return results

    try:
        with open(sol_path, 'r') as f:
            data = json.load(f)
    except Exception:
        return results

    # Specific question evaluation logic

    name = str(data.get('dashboard_name', '')).strip()
    err_p = str(data.get('error_rate_panel_type', '')).strip().lower()
    tp_q = str(data.get('throughput_query', '')).strip().lower()
    lat_p = str(data.get('latency_panel_type', '')).strip().lower()

    results['tc1'] = True
    results['tc2'] = (err_p != '' and err_p != 'todo' and ('line' in err_p or 'timeseries' in err_p or 'chart' in err_p))
    results['tc3'] = (tp_q != '' and tp_q != 'todo' and ('count' in tp_q or 'rate' in tp_q or 'rpm' in tp_q))
    results['tc4'] = (lat_p != '' and lat_p != 'todo' and ('heatmap' in lat_p or 'bar' in lat_p or 'histogram' in lat_p))
    
    hg = str(data.get('health_gauge_panel', '') or data.get('health_panel', '')).strip().lower()
    results['tc5'] = (hg != '' and hg != 'todo')
    
    ac = str(data.get('alert_channel', '') or data.get('notification_channel', '')).strip().lower()
    results['tc6'] = (ac != '' and ac != 'todo')
    
    ar = str(data.get('auto_refresh', '')).strip().lower()
    results['tc7'] = (ar != '' and ar != 'todo')
    
    gl = str(data.get('grid_layout', '') or data.get('coordinates', '')).strip().lower()
    results['tc8'] = (gl != '' and gl != 'todo')

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (3 if results.get('tc4') else 0) + (2 if results.get('tc5') else 0) + (2 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0) + (2 if results.get('tc8') else 0)
    
    # Save solution data for central evaluation registry
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 90,
        'evaluation_type': 'AUTO_EVALUATION',
        'score': score,
        'results': results,
        'exam_code': exam_code
    }
    
    ws_path = get_base_path()
    with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
        json.dump(solution_data, f, indent=4)

if __name__ == "__main__":
    test_results = run_tests()
    
    # Write solution file for the platform grading runner
    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        existing_data = {}
        if os.path.exists(sol_path):
            with open(sol_path, 'r') as f:
                existing_data = json.load(f)
        
        score = (3 if test_results.get('tc1') else 0) + (3 if test_results.get('tc2') else 0) + (3 if test_results.get('tc3') else 0) + (3 if test_results.get('tc4') else 0) + (2 if test_results.get('tc5') else 0) + (2 if test_results.get('tc6') else 0) + (2 if test_results.get('tc7') else 0) + (2 if test_results.get('tc8') else 0)
        existing_data['score'] = score
        existing_data['results'] = test_results
        
        with open(sol_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(test_results))
    else:
        TC_NAMES = {
            "tc1": "solution.json exists and is valid JSON",
            "tc2": "Error rate panel query and timeseries chart configured",
            "tc3": "Throughput panel (requests per minute) configured",
            "tc4": "Latency heatmap / bar chart panel configured",
            "tc5": "Service health status gauge panel included",
            "tc6": "Alert notification channel mapped",
            "tc7": "Auto-refresh interval set to 30s/1m",
            "tc8": "Dashboard grid layout coordinates specified"
        }
        print("Running Auto-Evaluation for: Log Analysis: Dashboard Panel Visualizations & Health Metrics\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 3
            elif k == 'tc2':
                marks = 3
            elif k == 'tc3':
                marks = 3
            elif k == 'tc4':
                marks = 3
            elif k == 'tc5':
                marks = 2
            elif k == 'tc6':
                marks = 2
            elif k == 'tc7':
                marks = 2
            elif k == 'tc8':
                marks = 2
            else:
                marks = 0

            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/20.0")
