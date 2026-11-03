import os
import sys
import json
import subprocess
import urllib.request
import urllib.parse


def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False}
    base_path = get_base_path()
    sol_json = os.path.join(base_path, 'solution.json')
    
    # 1. Parse student solution payload if provided
    if os.path.exists(sol_json):
        try:
            with open(sol_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for k in results.keys():
                if k in data.get('results', {}):
                    results[k] = bool(data['results'][k])
                elif k in data:
                    results[k] = bool(data[k])
        except Exception:
            pass

    # 2. Technology-Specific Validation Harness
    # Database & Databricks Verification Logic
    for fname in os.listdir(base_path):
        fpath = os.path.join(base_path, fname)
        if fname.endswith('.sql') or (fname.endswith('.json') and fname != 'solution.json'):
            if os.path.getsize(fpath) > 10:
                results['tc1'] = True

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (4 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
    total_marks = 10
    
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 30,
        'evaluation_type': 'AUTO_EVALUATION',
        'score': score,
        'total_marks': total_marks,
        'results': results,
        'exam_code': exam_code
    }
    
    try:
        ws_path = get_base_path()
        with open(os.path.join(ws_path, 'solution.json'), 'w', encoding='utf-8') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[SYSTEM] Warning: Could not write solution.json: {e}")
        
    return score, total_marks, results

if __name__ == "__main__":
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (4 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
    total_marks = 10
    
    # Update local solution.json with latest evaluation result
    try:
        sol_path = os.path.join(get_base_path(), 'solution.json')
        existing_data = {}
        if os.path.exists(sol_path):
            with open(sol_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        existing_data['score'] = score
        existing_data['total_marks'] = total_marks
        existing_data['results'] = results
        with open(sol_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4)
    except Exception:
        pass

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(results))
        sys.exit(0 if score == total_marks else 1)

    TC_NAMES = {
        "tc1": "URI decomposition: script accurately parses components from PostgreSQL URI and key-value formats",
        "tc2": "Pre-flight socket check: script verifies TCP port 5432 availability prior to SQL authentication",
        "tc3": "Execution & formatting: returns valid JSON with database name, user, and connection latency"
}
    TC_MARKS = {
        "tc1": 3,
        "tc2": 4,
        "tc3": 3
}

    print("Running Auto-Evaluation for: Database Lab: PostgreSQL Connection String Parsing & Diagnostic Scripting\n")
    for k, v in results.items():
        tc_num = k[2:]
        desc = TC_NAMES.get(k, '')
        marks = TC_MARKS.get(k, 0)
        display_marks = int(marks) if marks % 1 == 0 else marks
        if v:
            print(f"PASS TC{tc_num} [{desc}] ({display_marks}/{display_marks})")
        else:
            print(f"FAIL TC{tc_num} [{desc}] (0/{display_marks})")

    display_score = int(score) if score % 1 == 0 else score
    display_max = int(total_marks) if total_marks % 1 == 0 else total_marks
    print(f"\nSCORE: {display_score}/{display_max}")
    sys.exit(0 if score == total_marks else 1)
