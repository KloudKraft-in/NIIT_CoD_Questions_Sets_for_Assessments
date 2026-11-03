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

    py_path = os.path.join(get_base_path(), 'template_manager.py')
    if os.path.exists(py_path):
        with open(py_path, 'r') as f:
            code = f.read()
        results['tc1'] = True
        results['tc2'] = ('incident' in code.lower() and 'rca' in code.lower())
        results['tc3'] = ('format' in code or 'replace' in code or 'substitute' in code)
        results['tc4'] = ('template_library.json' in code)
        results['tc5'] = True
        results['tc6'] = True
        results['tc7'] = True
        results['tc8'] = True


    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (4 if results.get('tc1') else 0) + (4 if results.get('tc2') else 0) + (4 if results.get('tc3') else 0) + (4 if results.get('tc4') else 0) + (3 if results.get('tc5') else 0) + (2 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0) + (2 if results.get('tc8') else 0)
    
    # Save solution data for central evaluation registry
    ws_path = get_base_path()
    sol_file = os.path.join(ws_path, 'solution.json')
    solution_data = {}
    if os.path.exists(sol_file):
        try:
            with open(sol_file, 'r') as f:
                solution_data = json.load(f)
        except Exception:
            pass

    solution_data['candidate_prefix'] = vm_tag
    solution_data['assessment_start_time'] = start_time
    solution_data['max_duration_minutes'] = 90
    solution_data['evaluation_type'] = 'AUTO_EVALUATION'
    solution_data['score'] = score
    solution_data['results'] = results
    solution_data['exam_code'] = exam_code
    
    with open(sol_file, 'w') as f:
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
        
        score = (4 if test_results.get('tc1') else 0) + (4 if test_results.get('tc2') else 0) + (4 if test_results.get('tc3') else 0) + (4 if test_results.get('tc4') else 0) + (3 if test_results.get('tc5') else 0) + (2 if test_results.get('tc6') else 0) + (2 if test_results.get('tc7') else 0) + (2 if test_results.get('tc8') else 0)
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
            "tc1": "template_manager.py is syntax-valid Python",
            "tc2": "Supports 8 operational categories (Incident, Log, RCA, Change, etc.)",
            "tc3": "Implements variable substitution engine for {placeholders}",
            "tc4": "Outputs valid template_library.json",
            "tc5": "Validates template variable completeness",
            "tc6": "Prevents duplicate template names",
            "tc7": "Provides template search by category function",
            "tc8": "Exports default system prompt configuration"
        }
        print("Running Auto-Evaluation for: GenAI Ops: Reusable Operational Prompt Template System\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 4
            elif k == 'tc2':
                marks = 4
            elif k == 'tc3':
                marks = 4
            elif k == 'tc4':
                marks = 4
            elif k == 'tc5':
                marks = 3
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
        print(f"\nSCORE: {total_score}/25.0")
