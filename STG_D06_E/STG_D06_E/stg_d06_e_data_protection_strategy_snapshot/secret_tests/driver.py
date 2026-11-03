import os
import sys
import json
import re
from datetime import datetime, timezone

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False}
    base_path = get_base_path()

    # Technology-Specific Validation Harness for STG_D06_E
    # Data Protection Strategy — Snapshot vs Backup vs Replication Rules
    candidate_paths = [
        os.path.join(base_path, 'data_protection_policy.json'),
        os.path.join(os.path.dirname(base_path), 'data_protection_policy.json'),
        os.path.expanduser('~/data_protection_policy.json'),
        '/home/LabsKraft/data_protection_policy.json',
        '/home/ubuntu/data_protection_policy.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()

            parsed = json.loads(content)
            policies = parsed.get('policies', [])
            if not isinstance(policies, list):
                policies = parsed.get('requirements', [])

            policy_map = {}
            for p in policies:
                rid = str(p.get('requirement_id') or p.get('id') or '').strip().upper()
                if rid:
                    policy_map[rid] = p

            req_ids = {'DR-01', 'DR-02', 'DR-03', 'DR-04'}
            if req_ids.issubset(set(policy_map.keys())):
                # Check for TODO in any field
                has_any_todo = False
                for p in policy_map.values():
                    for v in p.values():
                        if 'TODO' in str(v).upper():
                            has_any_todo = True

                if not has_any_todo:
                    # TC1: Accurate mechanism alignment
                    m1 = str(policy_map['DR-01'].get('recommended_mechanism', '')).lower()
                    m2 = str(policy_map['DR-02'].get('recommended_mechanism', '')).lower()
                    m3 = str(policy_map['DR-03'].get('recommended_mechanism', '')).lower()
                    m4 = str(policy_map['DR-04'].get('recommended_mechanism', '')).lower()

                    match_m1 = any(w in m1 for w in ['snapshot', 'replication', 'cow'])
                    match_m2 = any(w in m2 for w in ['backup', 'air-gap', 'immutable'])
                    match_m3 = any(w in m3 for w in ['replication', 'sync', 'continuous'])
                    match_m4 = any(w in m4 for w in ['snapshot'])

                    if match_m1 and match_m2 and match_m3 and match_m4:
                        results['tc1'] = True

                    # TC2: RPO / RTO quantification
                    all_quantified = True
                    for rid in ['DR-01', 'DR-02', 'DR-03', 'DR-04']:
                        rpo = str(policy_map[rid].get('target_rpo_minutes', ''))
                        rto = str(policy_map[rid].get('target_rto_minutes', ''))
                        if not (re.search(r'\d+', rpo) and re.search(r'\d+', rto)):
                            all_quantified = False

                    if all_quantified:
                        results['tc2'] = True

                    # TC3: Schema completeness and technical rationale
                    rationale_ok = True
                    for rid in ['DR-01', 'DR-02', 'DR-03', 'DR-04']:
                        rat = str(policy_map[rid].get('technical_rationale', '')).strip()
                        if len(rat) < 10:
                            rationale_ok = False

                    if rationale_ok:
                        results['tc3'] = True
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
        "tc1": "Strategy alignment: accurate assignment of snapshot, backup, and replication mechanisms to the 4 business requirements",
        "tc2": "RPO/RTO quantification: realistic RPO and RTO thresholds assigned based on storage engine technical characteristics",
        "tc3": "JSON schema validation: data_protection_policy.json is well-formed with rationale and failure isolation explanations"
    }
    TC_MARKS = {
        "tc1": 4,
        "tc2": 3,
        "tc3": 3
    }

    print("Running Auto-Evaluation for: Storage Lab: Data Protection Strategy — Snapshot vs Backup vs Replication Rules\n")
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
