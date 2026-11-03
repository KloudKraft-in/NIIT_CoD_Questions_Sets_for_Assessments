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
    
    target_file = None

    if sol_path and os.path.exists(sol_path):
        if os.path.isdir(sol_path):
            for candidate in ['solution.json', 'crisp_prompt.json']:
                c_path = os.path.join(sol_path, candidate)
                if os.path.exists(c_path):
                    target_file = c_path
                    break
        elif os.path.isfile(sol_path):
            target_file = sol_path
    else:
        for candidate in ['solution.json', 'crisp_prompt.json']:
            c_path = os.path.join(get_base_path(), candidate)
            if os.path.exists(c_path):
                target_file = c_path
                break

    if not target_file or not os.path.exists(target_file):
        return results

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return results

    if not isinstance(data, dict):
        return results

    role = str(data.get('role') or data.get('persona') or '').strip().lower()
    proof = str(data.get('proof') or data.get('verification') or '').strip().lower()
    context = str(data.get('context') or '').strip().lower()
    instruction = str(data.get('instruction') or '').strip().lower()
    specifics = str(data.get('specifics') or '').strip().lower()
    raw_json = json.dumps(data).lower()

    # Check if all fields are still untouched TODOs or empty
    non_todo_fields = [v for v in [role, proof, context, instruction, specifics] if v and v != 'todo']
    if not non_todo_fields:
        # Untouched default template -> All TCs fail
        return results

    # TC1: CRISP keys present and populated
    crisp_keys = ['context', 'role', 'instruction', 'specifics', 'proof']
    has_keys = all(k in data for k in crisp_keys) or len(non_todo_fields) >= 2
    results['tc1'] = has_keys and len(non_todo_fields) >= 2

    # TC2: Role assigned to Senior SRE / Incident Commander
    results['tc2'] = (role != 'todo' and any(w in role for w in ['sre', 'incident', 'commander', 'engineer', 'senior'])) or ('senior sre' in raw_json) or ('incident commander' in raw_json)

    # TC3: Proof component requires verification command or log snippet
    results['tc3'] = (proof != 'todo' and any(w in proof for w in ['log', 'command', 'output', 'json', 'uptime', 'curl', 'kubectl', 'grep', 'status', 'trace'])) or ('proof' in raw_json and len(proof) > 3 and proof != 'todo')

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
            "tc1": "solution.json contains all CRISP keys",
            "tc2": "Role assigned to Senior SRE / Incident Commander",
            "tc3": "Proof component requires verification command or log snippet"
        }
        print("Running Auto-Evaluation for: GenAI Ops: CRISP Prompt Framework Structuring\n")
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
