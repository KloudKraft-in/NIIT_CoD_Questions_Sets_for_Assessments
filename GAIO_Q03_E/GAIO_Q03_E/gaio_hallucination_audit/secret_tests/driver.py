import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests(sol_path=None):
    results = {
        "tc1": False,
        "tc2": False,
        "tc3": False
    }
    
    if not sol_path or not os.path.exists(sol_path):
        for name in ['command_audit.json', 'solution.json']:
            candidate = os.path.join(get_base_path(), name)
            if os.path.exists(candidate):
                sol_path = candidate
                break
                
    if not sol_path or not os.path.exists(sol_path):
        return results

    if os.path.isdir(sol_path):
        for name in ['command_audit.json', 'solution.json']:
            candidate = os.path.join(sol_path, name)
            if os.path.exists(candidate):
                sol_path = candidate
                break

    if os.path.isdir(sol_path):
        return results

    try:
        with open(sol_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return results

    if isinstance(data, dict):
        flags = [str(f).strip().lower() for f in (data.get('fake_flags') or data.get('fabricated_flags') or data.get('flags') or [])]
        cmds = [str(c).strip().lower() for c in (data.get('hallucinated_commands') or data.get('fake_commands') or data.get('commands') or [])]
        raw_json = json.dumps(data).lower()

        results['tc1'] = True
        results['tc2'] = any('--force-push-all' in f for f in flags) or ('--force-push-all' in raw_json)
        results['tc3'] = any('sysclean-all' in c for c in cmds) or ('sysclean-all' in raw_json)

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (4 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
    
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
    solution_data['max_duration_minutes'] = 30
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
        
        score = (3 if test_results.get('tc1') else 0) + (4 if test_results.get('tc2') else 0) + (3 if test_results.get('tc3') else 0)
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
            "tc1": "command_audit.json exists",
            "tc2": "Fabricated flag '--force-push-all' identified",
            "tc3": "Non-existent command 'sysclean-all' marked as hallucinated"
        }
        print("Running Auto-Evaluation for: GenAI Ops: Recognizing AI Hallucinations in CLI Commands\n")
        total_score = 0
        for k, v in test_results.items():
            tc_num = k[2:]
            desc = TC_NAMES.get(k, '')
            if k == 'tc1':
                marks = 3
            elif k == 'tc2':
                marks = 4
            elif k == 'tc3':
                marks = 3
            elif k == 'tc4':
                marks = 0
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
        print(f"\nSCORE: {total_score}/10.0")
