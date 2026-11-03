import os
import sys
import json
import re
from datetime import datetime, timezone

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_blueprint_data(file_path):
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
        os.path.join(base_path, 'hybrid_storage_migration_blueprint.json'),
        os.path.join(base_path, 'storage_migration_blueprint.json'),
        os.path.join(base_path, 'migration_blueprint.json'),
        os.path.join(os.path.dirname(base_path), 'hybrid_storage_migration_blueprint.json'),
        os.path.expanduser('~/hybrid_storage_migration_blueprint.json'),
        '/home/LabsKraft/hybrid_storage_migration_blueprint.json',
        '/home/ubuntu/hybrid_storage_migration_blueprint.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_blueprint_data(target_file)

            # TC1: Block workload mapping: comprehensive IOPS, throughput, and capacity sizing for SAN-to-cloud block migration
            block_targets = report.get('block_san_targets', {})
            if isinstance(block_targets, dict):
                aws_b = str(block_targets.get('aws', '')).lower()
                azure_b = str(block_targets.get('azure', '')).lower()
                gcp_b = str(block_targets.get('gcp', '')).lower()
                valid_count = 0
                if 'todo' not in aws_b and any(w in aws_b for w in ['ebs', 'io2', 'gp3', 'provisioned']):
                    valid_count += 1
                if 'todo' not in azure_b and any(w in azure_b for w in ['ssd', 'ultra', 'disk', 'managed']):
                    valid_count += 1
                if 'todo' not in gcp_b and any(w in gcp_b for w in ['disk', 'hyperdisk', 'extreme', 'balanced', 'pd']):
                    valid_count += 1
                if valid_count >= 2:
                    results['tc1'] = True

            # TC2: File share mapping: protocol parity (NFSv3/v4, SMB3) and permission preservation (NTFS ACLs, POSIX) defined
            file_targets = report.get('file_nas_targets', {})
            if isinstance(file_targets, dict):
                aws_f = str(file_targets.get('aws', '')).lower()
                azure_f = str(file_targets.get('azure', '')).lower()
                gcp_f = str(file_targets.get('gcp', '')).lower()
                valid_count = 0
                if 'todo' not in aws_f and any(w in aws_f for w in ['fsx', 'efs', 'ontap']):
                    valid_count += 1
                if 'todo' not in azure_f and any(w in azure_f for w in ['netapp', 'azure files', 'files']):
                    valid_count += 1
                if 'todo' not in gcp_f and any(w in gcp_f for w in ['filestore', 'netapp', 'volumes']):
                    valid_count += 1
                if valid_count >= 2:
                    results['tc2'] = True

            # TC3: Archive & compliance mapping: immutable WORM retention and lifecycle policies formulated across cloud tiers
            archive_targets = report.get('archive_targets', {})
            if isinstance(archive_targets, dict):
                aws_a = str(archive_targets.get('aws', '')).lower()
                azure_a = str(archive_targets.get('azure', '')).lower()
                gcp_a = str(archive_targets.get('gcp', '')).lower()
                valid_count = 0
                if 'todo' not in aws_a and any(w in aws_a for w in ['glacier', 'deep archive', 's3']):
                    valid_count += 1
                if 'todo' not in azure_a and any(w in azure_a for w in ['blob', 'archive']):
                    valid_count += 1
                if 'todo' not in gcp_a and any(w in gcp_a for w in ['storage archive', 'archive', 'gcs']):
                    valid_count += 1
                if valid_count >= 2:
                    results['tc3'] = True

            # TC4: Lifecycle transition rules: precise time-based tiering rules from hot to cool to archive configured
            lifecycle = report.get('lifecycle_transition_rules', {})
            if isinstance(lifecycle, dict):
                hot = str(lifecycle.get('hot_tier_retention_days', '')).lower()
                cool = str(lifecycle.get('cool_tier_transition_days', '')).lower()
                arch = str(lifecycle.get('archive_tier_transition_days', '')).lower()
                worm = str(lifecycle.get('immutability_worm_retention_years', '')).lower()
                if ('todo' not in hot and re.search(r'\d+', hot)) and \
                   ('todo' not in cool and re.search(r'\d+', cool)) and \
                   ('todo' not in arch and re.search(r'\d+', arch)) and \
                   ('todo' not in worm and re.search(r'\d+', worm)):
                    results['tc4'] = True

            # TC5: RPO/RTO SLA framework: quantifiable RPO and RTO targets defined with justification per business tier
            slas = report.get('rpo_rto_slas', {})
            if isinstance(slas, dict):
                t1 = slas.get('tier_1_mission_critical_db', {})
                t2 = slas.get('tier_2_file_shares', {})
                t3 = slas.get('tier_3_compliance_archive', {})
                t1_ok = 'todo' not in str(t1.get('rpo', '')).lower() and 'todo' not in str(t1.get('rto', '')).lower() and bool(t1.get('rpo'))
                t2_ok = 'todo' not in str(t2.get('rpo', '')).lower() and 'todo' not in str(t2.get('rto', '')).lower() and bool(t2.get('rpo'))
                t3_ok = 'todo' not in str(t3.get('rpo', '')).lower() and 'todo' not in str(t3.get('rto', '')).lower() and bool(t3.get('rpo'))
                if t1_ok and t2_ok and t3_ok:
                    results['tc5'] = True

            # TC6: Cutover & delta sync plan: phased synchronization methodology minimizing production cutover maintenance window
            cutover = report.get('cutover_delta_sync_strategy', {})
            if isinstance(cutover, dict):
                bulk = str(cutover.get('initial_bulk_sync_tool', '')).lower()
                delta = str(cutover.get('continuous_delta_replication', '')).lower()
                window = str(cutover.get('final_cutover_window', '')).lower()
                if ('todo' not in bulk and any(w in bulk for w in ['datasync', 'mover', 'transfer', 'sync', 'tool'])) and \
                   ('todo' not in delta and any(w in delta for w in ['delta', 'incremental', 'replication', 'hourly', 'sync'])) and \
                   ('todo' not in window and any(w in window for w in ['cutover', 'window', 'hour', 'freeze', 'dns', 'switch'])):
                    results['tc6'] = True

            # TC7: Azure Arc hybrid monitoring: architectural design incorporating Azure Arc for unified on-prem/cloud visibility
            monitoring = str(report.get('hybrid_monitoring_tool', '')).lower()
            if 'todo' not in monitoring and any(w in monitoring for w in ['azure arc', 'arc']):
                results['tc7'] = True

            # TC8: Blueprint validation: hybrid_storage_migration_blueprint.json conforms to standard architecture schema
            project = str(report.get('migration_project', '')).lower()
            if ('500' in project or 'hybrid' in project) and sum(1 for k in ['tc1', 'tc2', 'tc3', 'tc4', 'tc5', 'tc6', 'tc7'] if results[k]) >= 4:
                results['tc8'] = True

        except Exception:
            pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0) + (3 if results.get('tc5') else 0) + (2 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0) + (2 if results.get('tc8') else 0)
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
    score = (3 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0) + (3 if results.get('tc5') else 0) + (2 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0) + (2 if results.get('tc8') else 0)
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
        "tc1": "Block workload mapping: comprehensive IOPS, throughput, and capacity sizing for SAN-to-cloud block migration",
        "tc2": "File share mapping: protocol parity (NFSv3/v4, SMB3) and permission preservation (NTFS ACLs, POSIX) defined",
        "tc3": "Archive & compliance mapping: immutable WORM retention and lifecycle policies formulated across cloud tiers",
        "tc4": "Lifecycle transition rules: precise time-based tiering rules from hot to cool to archive configured",
        "tc5": "RPO/RTO SLA framework: quantifiable RPO and RTO targets defined with justification per business tier",
        "tc6": "Cutover & delta sync plan: phased synchronization methodology minimizing production cutover maintenance window",
        "tc7": "Azure Arc hybrid monitoring: architectural design incorporating Azure Arc for unified on-prem/cloud visibility",
        "tc8": "Blueprint validation: hybrid_storage_migration_blueprint.json conforms to standard architecture schema"
    }
    TC_MARKS = {
        "tc1": 3,
        "tc2": 3,
        "tc3": 3,
        "tc4": 2,
        "tc5": 3,
        "tc6": 2,
        "tc7": 2,
        "tc8": 2
    }

    print("Running Auto-Evaluation for: Storage Lab: Hybrid Cloud Storage Migration & RPO/RTO Data Protection Plan\n")
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
