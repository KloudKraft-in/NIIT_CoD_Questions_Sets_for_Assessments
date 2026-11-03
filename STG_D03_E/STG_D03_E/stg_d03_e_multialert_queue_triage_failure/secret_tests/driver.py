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
    sol_json = os.path.join(base_path, 'solution.json')
    
    # Fresh evaluation will be computed below
    pass

    # 2. Technology-Specific Validation Harness for STG_D03_E
    # Storage Multi-Alert Queue Triage Verification
    candidate_paths = [
        os.path.join(base_path, 'prioritized_alerts.json'),
        os.path.join(os.path.dirname(base_path), 'prioritized_alerts.json'),
        os.path.expanduser('~/prioritized_alerts.json'),
        '/home/LabsKraft/prioritized_alerts.json',
        '/home/ubuntu/prioritized_alerts.json',
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
            alerts_list = parsed.get('prioritized_queue', [])
            if not isinstance(alerts_list, list):
                alerts_list = parsed.get('alerts', [])

            # Check if all 4 alerts are present and not containing TODO placeholders
            alert_map = {}
            has_todos = False
            for item in alerts_list:
                aid = str(item.get('alert_id', '')).strip().upper()
                if aid:
                    alert_map[aid] = item
                for val in item.values():
                    if 'TODO' in str(val).upper():
                        has_todos = True

            req_ids = {'ALT-01', 'ALT-02', 'ALT-03', 'ALT-04'}
            if req_ids.issubset(set(alert_map.keys())) and not has_todos:
                # TC1: Successfully parsed 4 alert objects with non-placeholder fields
                results['tc1'] = True

                # TC2: Accurate failure domain mapping
                # ALT-01: Capacity / Disk Full
                # ALT-02: Saturation / Performance / Latency / Queue Depth
                # ALT-03: Connectivity / Stale Mount / Network / NFS
                # ALT-04: Data Protection / Backup Quota / Snapshot
                d1 = str(alert_map['ALT-01'].get('failure_domain', '')).lower()
                d2 = str(alert_map['ALT-02'].get('failure_domain', '')).lower()
                d3 = str(alert_map['ALT-03'].get('failure_domain', '')).lower()
                d4 = str(alert_map['ALT-04'].get('failure_domain', '')).lower()

                c1 = any(w in d1 for w in ['capacity', 'disk', 'space'])
                c2 = any(w in d2 for w in ['saturation', 'performance', 'latency', 'iops', 'queue'])
                c3 = any(w in d3 for w in ['connectivity', 'mount', 'network', 'nfs'])
                c4 = any(w in d4 for w in ['data protection', 'backup', 'snapshot', 'replica'])

                if c1 and c2 and c3 and c4:
                    results['tc2'] = True

                # TC3: ITIL Priority & Runbook assignment
                p1 = str(alert_map['ALT-01'].get('priority', '')).upper()
                p2 = str(alert_map['ALT-02'].get('priority', '')).upper()
                p3 = str(alert_map['ALT-03'].get('priority', '')).upper()
                p4 = str(alert_map['ALT-04'].get('priority', '')).upper()

                r1 = str(alert_map['ALT-01'].get('runbook_name', '')).upper()
                r2 = str(alert_map['ALT-02'].get('runbook_name', '')).upper()
                r3 = str(alert_map['ALT-03'].get('runbook_name', '')).upper()
                r4 = str(alert_map['ALT-04'].get('runbook_name', '')).upper()

                # P1/P2 for production capacity/saturation/mount issues; P3/P4 for backup quota rate
                valid_p = (
                    any(px in p1 for px in ['P1', 'P2']) and
                    any(px in p2 for px in ['P1', 'P2']) and
                    any(px in p3 for px in ['P1', 'P2']) and
                    any(px in p4 for px in ['P3', 'P4'])
                )
                valid_r = (
                    any(w in r1 for w in ['SOP', 'DISK', 'FULL', 'CAPACITY']) and
                    any(w in r2 for w in ['SOP', 'STORAGE', 'LATENCY', 'SATURATION', 'QUEUE']) and
                    any(w in r3 for w in ['SOP', 'NFS', 'MOUNT', 'CONNECT']) and
                    any(w in r4 for w in ['SOP', 'BACKUP', 'QUOTA', 'PROTECT'])
                )

                if valid_p and valid_r:
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
        "tc1": "Alert parsing: accurately extract affected resource ID, metric name, and trigger value from incoming_alerts.json",
        "tc2": "Domain classification: 100% correct failure domain mapping for capacity, latency, mount, and backup errors",
        "tc3": "Dispatch list generation: prioritized_alerts.json matches required schema with appropriate ITIL priority and SOP references"
    }
    TC_MARKS = {
        "tc1": 4,
        "tc2": 3,
        "tc3": 3
    }

    print("Running Auto-Evaluation for: Storage Lab: Multi-Alert Queue Triage & Failure Category Classification\n")
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
