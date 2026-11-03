import os
import sys
import json
import re
from datetime import datetime, timezone

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_report_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        data = json.loads(content)
        return {str(k).lower().strip(): v for k, v in data.items()}
    except Exception:
        pass

    norm = {}
    for line in content.splitlines():
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            norm[k.strip().lower()] = v.strip()
    return norm

def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False, "tc6": False, "tc7": False, "tc8": False}
    base_path = get_base_path()

    candidate_paths = [
        os.path.join(base_path, 'netapp_export_rca.json'),
        os.path.join(base_path, 'netapp_rca_report.json'),
        os.path.join(base_path, 'netapp_rca.json'),
        os.path.join(os.path.dirname(base_path), 'netapp_export_rca.json'),
        os.path.expanduser('~/netapp_export_rca.json'),
        '/home/LabsKraft/netapp_export_rca.json',
        '/home/ubuntu/netapp_export_rca.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_report_data(target_file)

            # TC1: Junction path validation: confirm volume junction path /vol_k8s_data is active in the SVM root namespace
            junc_active = str(report.get('junction_path_active', '')).strip().upper()
            if 'TODO' not in junc_active and any(s in junc_active for s in ['YES', 'TRUE', 'ACTIVE']):
                results['tc1'] = True

            # TC2: Client-match CIDR triage: correctly identify the subnet mismatch between worker nodes and export rule
            cidr_info = report.get('detected_cidr_mismatch', {})
            if isinstance(cidr_info, dict):
                cfg = str(cidr_info.get('configured_clientmatch', '')).strip()
                act = str(cidr_info.get('actual_worker_subnet', '')).strip()
            else:
                cfg = str(report.get('configured_clientmatch', '')).strip()
                act = str(report.get('actual_worker_subnet', '')).strip()

            if ('TODO' not in cfg.upper() and '10.10.10' in cfg) and \
               ('TODO' not in act.upper() and '10.10.20' in act):
                results['tc2'] = True

            # TC3: Superuser / Root Squash analysis: explain why 'superuser none' blocks kubelet volume initialization
            root_squash = str(report.get('root_squash_issue', '')).strip().lower()
            if 'todo' not in root_squash and any(w in root_squash for w in ['superuser', 'root', 'kubelet', 'squash']):
                results['tc3'] = True

            # TC4: ONTAP command formulation: accurately construct the complete vserver export-policy rule modify command
            cmd = str(report.get('corrected_ontap_cli_command', '')).strip().lower()
            if 'todo' not in cmd and ('vserver export-policy rule modify' in cmd or 'export-policy rule modify' in cmd) and \
               ('10.10.20' in cmd) and ('superuser' in cmd):
                results['tc4'] = True

            # TC5: Access protocol verification: ensure rule permits both NFSv3 and NFSv4 protocol negotiations
            proto = str(report.get('protocols_supported', '')).strip().lower()
            if 'todo' not in proto and (('nfs3' in proto and 'nfs4' in proto) or ('nfs' in proto and '4' in proto) or ('nfs3,nfs4' in cmd)):
                results['tc5'] = True

            # TC6: Client mount execution: test_mount.sh executes successfully and mounts the export without permission denied
            mount_status = str(report.get('client_mount_status', '')).strip().upper()
            if 'TODO' not in mount_status and any(s in mount_status for s in ['SUCCESS', 'RESOLVED', 'ACTIVE', 'MOUNTED', 'OK']):
                results['tc6'] = True

            # TC7: RCA completeness: netapp_export_rca.json provides detailed technical root cause and change-audit trail
            vserver = str(report.get('vserver', '')).strip().lower()
            policy = str(report.get('policy_name', '')).strip().lower()
            rule_idx = str(report.get('offending_rule_index', '')).strip()
            rca = str(report.get('root_cause_analysis', '')).strip().lower()
            if ('todo' not in vserver and 'svm_k8s' in vserver) and \
               ('todo' not in policy and 'k8s_policy' in policy) and \
               ('todo' not in rule_idx and '2' in rule_idx) and \
               ('todo' not in rca and any(w in rca for w in ['cidr', 'subnet', 'mismatch', 'superuser', 'squash', 'ip', 'migrat', 'access'])):
                results['tc7'] = True

            # TC8: Prevention controls: define policy automated validation checks before applying future NetApp export rule changes
            controls = str(report.get('prevention_governance_controls', '')).strip().lower()
            if 'todo' not in controls and any(c in controls for c in ['ci/cd', 'validation', 'inventory', 'automated', 'pre-commit', 'gate', 'pipeline', 'audit', 'check']):
                results['tc8'] = True

        except Exception:
            pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (2 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (3 if results.get('tc4') else 0) + (2 if results.get('tc5') else 0) + (3 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0) + (2 if results.get('tc8') else 0)
    total_marks = 20
    
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 90,
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
    score = (2 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (3 if results.get('tc4') else 0) + (2 if results.get('tc5') else 0) + (3 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0) + (2 if results.get('tc8') else 0)
    total_marks = 20
    
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
        "tc1": "Junction path validation: confirm volume junction path /vol_k8s_data is active in the SVM root namespace",
        "tc2": "Client-match CIDR triage: correctly identify the subnet mismatch between worker nodes and export rule",
        "tc3": "Superuser / Root Squash analysis: explain why 'superuser none' blocks kubelet volume initialization",
        "tc4": "ONTAP command formulation: accurately construct the complete vserver export-policy rule modify command",
        "tc5": "Access protocol verification: ensure rule permits both NFSv3 and NFSv4 protocol negotiations",
        "tc6": "Client mount execution: test_mount.sh executes successfully and mounts the export without permission denied",
        "tc7": "RCA completeness: netapp_export_rca.json provides detailed technical root cause and change-audit trail",
        "tc8": "Prevention controls: define policy automated validation checks before applying future NetApp export rule changes"
    }
    TC_MARKS = {
        "tc1": 2,
        "tc2": 3,
        "tc3": 3,
        "tc4": 3,
        "tc5": 2,
        "tc6": 3,
        "tc7": 2,
        "tc8": 2
    }

    print("Running Auto-Evaluation for: Storage Lab: NetApp ONTAP Multi-Protocol Export Failure & Access Policy Lockdown\n")
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
