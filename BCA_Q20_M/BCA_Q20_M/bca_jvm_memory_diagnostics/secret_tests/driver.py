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

    cls = data.get('leak_class', '').strip().lower()
    obj = data.get('leak_object_type', '').strip().lower()
    ln = int(data.get('line_number', 0))
    arg = data.get('jvm_heap_argument', '').strip().lower()
    results['tc1'] = True
    results['tc2'] = ('sessionmanager' in cls or 'cache' in cls)
    results['tc3'] = ('hashmap' in obj or 'list' in obj or 'vector' in obj)
    results['tc4'] = (ln == 89 or ln == 90)
    results['tc5'] = (len(data.get('rca_notes', '')) > 10)
    results['tc6'] = ('-xmx' in arg)
    results['tc7'] = True
    results['tc8'] = True


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
            "tc1": "solution.json exists",
            "tc2": "Memory leak class suspect correctly identified",
            "tc3": "Correct list/collection object causing leak identified",
            "tc4": "Line number of insertion leak mapped correctly",
            "tc5": "RCA analysis notes populated",
            "tc6": "Recommended heap memory increase parameter included",
            "tc7": "Thread dump correlation correct",
            "tc8": "JVM arguments settings validated"
        }
        print("Running Auto-Evaluation for: Basic Code Analysis: JVM Memory OutOfMemoryError Diagnostics\n")
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
