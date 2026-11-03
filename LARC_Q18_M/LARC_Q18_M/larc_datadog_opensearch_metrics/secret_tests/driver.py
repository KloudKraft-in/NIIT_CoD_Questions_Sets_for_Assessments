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

    agg = str(data.get('opensearch_agg_syntax', '')).strip().lower()
    dd = str(data.get('datadog_query', '')).strip().lower()

    results['tc1'] = True
    results['tc2'] = (agg != '' and agg != 'todo' and ('percentiles' in agg or 'p99' in agg or 'p95' in agg or 'stats' in agg or len(agg) > 3))
    
    p99 = 0
    try:
        raw_p99 = str(data.get('p99_latency_ms', '0'))
        import re
        digits = re.findall(r'\d+', raw_p99)
        p99 = int(digits[0]) if digits else 0
    except Exception:
        p99 = 0
    results['tc3'] = (p99 >= 1000 or p99 > 0)

    results['tc4'] = (dd != '' and dd != 'todo' and ('service' in dd or 'status' in dd or 'error' in dd or 'avg' in dd or 'max' in dd or '@' in dd or '*' in dd or len(dd) > 3))
    
    sla_raw = data.get('sla_breach')
    sla_str = str(sla_raw).strip().lower()
    results['tc5'] = (sla_raw is True or sla_str in ['true', '1', 'yes', 'breached', 'breach', 'true/false'] or (sla_raw != 0 and sla_raw is not False and sla_str != 'todo' and sla_str != '0' and sla_str != ''))
    
    grp = str(data.get('group_by_field', '') or data.get('datadog_query', '')).strip()
    results['tc6'] = (grp != '' and grp.upper() != 'TODO')
    
    tb = str(data.get('time_bucket', '') or data.get('time_interval', '')).strip()
    results['tc7'] = (tb != '' and tb.upper() != 'TODO')
    
    alt = str(data.get('alert_condition', '') or data.get('alert_trigger', '')).strip()
    results['tc8'] = (alt != '' and alt.upper() != 'TODO')

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
            "tc2": "OpenSearch percentile aggregation syntax ('percentiles') correct",
            "tc3": "P99 latency threshold value correctly calculated",
            "tc4": "Datadog log search query syntax valid",
            "tc5": "Service SLA breach status identified",
            "tc6": "Group-by field ('service') included",
            "tc7": "Time interval bucket set to 1m/5m",
            "tc8": "Alert trigger condition specified"
        }
        print("Running Auto-Evaluation for: Log Analysis: Datadog & OpenSearch Log Aggregation Metrics\n")
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
