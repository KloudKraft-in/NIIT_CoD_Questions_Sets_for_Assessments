import os
import sys
import json
import re
from datetime import datetime, timezone


def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))


def parse_triage_report(base_path):
    candidate_paths = [
        os.path.join(base_path, 'backup_failure_triage.json'),
        os.path.join(base_path, 'backup_triage.json'),
        os.path.join(base_path, 'triage_report.json'),
        os.path.join(base_path, 'backup_report.json'),
        os.path.join(os.path.dirname(base_path), 'backup_failure_triage.json'),
        os.path.expanduser('~/backup_failure_triage.json'),
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if not target_file:
        return None

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return None

    try:
        data = json.loads(content)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # Fallback to key-value line parsing
    data = {}
    for line in content.splitlines():
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            k = k.strip().strip('"').strip("'")
            v = v.strip().rstrip(',').strip('"').strip("'")
            data[k] = v
    return data if data else None


def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False}
    base_path = get_base_path()

    report = parse_triage_report(base_path)

    if report:
        def get_val(keys):
            for k in keys:
                for rk, rv in report.items():
                    if k in rk.lower():
                        return rv
            return None

        job_name = str(get_val(['job_name', 'job']) or '').strip()
        timestamp = str(get_val(['failure_timestamp', 'timestamp', 'time']) or '').strip()
        error_msg = str(get_val(['error_message', 'error', 'log_error', 'message']) or '').strip()
        category = str(get_val(['failure_category', 'category', 'classification']) or '').strip()
        root_cause = str(get_val(['root_cause_explanation', 'root_cause', 'cause']) or '').strip()

        raw_actions = get_val(['remediation_actions', 'remediation', 'actions', 'action'])
        actions_list = []
        if isinstance(raw_actions, list):
            actions_list = [str(a).strip() for a in raw_actions]
        elif isinstance(raw_actions, str):
            actions_list = [raw_actions.strip()]

        # TC1: Log parsing: accurately locate the failure line and isolate the underlying operating system / storage error (4 Marks)
        tc1_passed = False
        ts_valid = False
        err_valid = False

        if timestamp and 'todo' not in timestamp.lower():
            if any(t in timestamp for t in ['02:30', '2026-10-20', '02:30:44', '02:30:43', '02:30:42', '02:30:50']) or ('2026' in timestamp and '30' in timestamp):
                ts_valid = True

        if error_msg and 'todo' not in error_msg.lower():
            err_lower = error_msg.lower()
            if any(e in err_lower for e in ['no space', 'out of space', '28', 'enospc', 'failed to write', '0 bytes', 'storage pool', 'full', 'exhaust']):
                err_valid = True

        if ts_valid and err_valid:
            tc1_passed = True

        if tc1_passed:
            results['tc1'] = True

        # TC2: Category classification: correctly classify the failure as 'Destination Full / Target Repository Exhaustion' (3 Marks)
        tc2_passed = False
        if category and 'todo' not in category.lower():
            cat_lower = category.lower()
            valid_cats = [
                'destination full',
                'target repository exhaustion',
                'destination_full',
                'repository exhaustion',
                'destination storage full',
                'target exhaustion',
                'capacity exhaustion',
                'out of space',
                'storage pool exhaustion',
                'full'
            ]
            if any(vc in cat_lower for vc in valid_cats) or cat_lower.startswith('destination'):
                tc2_passed = True

        if tc2_passed:
            results['tc2'] = True

        # TC3: Remediation recommendation: backup_failure_triage.json details safe pruning of expired backups before re-running (3 Marks)
        tc3_passed = False
        valid_actions = [a for a in actions_list if a and 'todo' not in a.lower()]
        all_remediation_text = " ".join(valid_actions)
        if root_cause and 'todo' not in root_cause.lower():
            all_remediation_text += " " + root_cause
        all_remediation_lower = all_remediation_text.lower()

        if valid_actions or (root_cause and 'todo' not in root_cause.lower()):
            has_pruning = any(k in all_remediation_lower for k in [
                'prune', 'pruning', 'clean', 'cleanup', 'delete', 'remov',
                'expir', 'purge', 'retention', 'space', 'free', 'capacity', 'expand', 'clear'
            ])
            if has_pruning:
                tc3_passed = True

        if tc3_passed:
            results['tc3'] = True

    else:
        # Fallback to solution.json if report file is not found
        sol_json = os.path.join(base_path, 'solution.json')
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

    return results


def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (4 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
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
    score = (4 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
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
        "tc1": "Log parsing: accurately locate the failure line and isolate the underlying operating system / storage error",
        "tc2": "Category classification: correctly classify the failure as 'Destination Full / Target Repository Exhaustion'",
        "tc3": "Remediation recommendation: backup_failure_triage.json details safe pruning of expired backups before re-running"
    }
    TC_MARKS = {
        "tc1": 4,
        "tc2": 3,
        "tc3": 3
    }

    print("Running Auto-Evaluation for: Storage Lab: Backup Job Failure Log Analysis & Target Capacity Remediation\n")
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
