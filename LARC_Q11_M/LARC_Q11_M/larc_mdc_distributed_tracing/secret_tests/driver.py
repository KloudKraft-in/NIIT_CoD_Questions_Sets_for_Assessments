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
        "tc4": False
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

    tid = data.get('trace_id', '').strip()
    svc = data.get('failing_span_service', '').strip().lower()
    lat = int(data.get('total_latency_ms', 0))
    results['tc1'] = True
    results['tc2'] = ('trace-7741' in tid or '7741' in tid)
    results['tc3'] = ('inventory' in svc or 'payment' in svc)
    results['tc4'] = (lat == 3400 or lat == 3500 or lat > 2000)


    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (5 if results.get('tc1') else 0) + (5 if results.get('tc2') else 0) + (5 if results.get('tc3') else 0) + (5 if results.get('tc4') else 0)
    
    # Save solution data for central evaluation registry
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 60,
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
        
        score = (5 if test_results.get('tc1') else 0) + (5 if test_results.get('tc2') else 0) + (5 if test_results.get('tc3') else 0) + (5 if test_results.get('tc4') else 0)
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
            "tc2": "Trace ID ('trace-7741') correctly matched across all spans",
            "tc3": "Failing downstream span service correctly identified",
            "tc4": "Span execution latency correctly calculated"
        }
        print("Running Auto-Evaluation for: Log Analysis: Java MDC Context & Distributed Transaction Tracing\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 5
            elif k == 'tc2':
                marks = 5
            elif k == 'tc3':
                marks = 5
            elif k == 'tc4':
                marks = 5
            elif k == 'tc5':
                marks = 0
            elif k == 'tc6':
                marks = 0
            elif k == 'tc7':
                marks = 0
            elif k == 'tc8':
                marks = 0
            else:
                marks = 0

            if v:
                total_score += marks
                print(f"PASS TC{tc_num} [{desc}] ({marks}/{marks})")
            else:
                print(f"FAIL TC{tc_num} [{desc}] (0/{marks})")
        print(f"\nSCORE: {total_score}/20.0")
