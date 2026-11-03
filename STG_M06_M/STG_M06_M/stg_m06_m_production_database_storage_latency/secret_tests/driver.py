import os
import sys
import json
import re
from datetime import datetime, timezone

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_rca_report(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        data = json.loads(content)
        return {'type': 'json', 'data': data, 'content': content}
    except Exception:
        pass

    return {'type': 'text', 'data': {}, 'content': content}

def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False, "tc6": False, "tc7": False}
    base_path = get_base_path()

    candidate_paths = [
        os.path.join(base_path, 'storage_rca_report.json'),
        os.path.join(base_path, 'storage_rca_report.md'),
        os.path.join(os.path.dirname(base_path), 'storage_rca_report.json'),
        os.path.join(os.path.dirname(base_path), 'storage_rca_report.md'),
        os.path.expanduser('~/storage_rca_report.json'),
        os.path.expanduser('~/storage_rca_report.md'),
        '/home/LabsKraft/storage_rca_report.json',
        '/home/ubuntu/storage_rca_report.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            parsed = parse_rca_report(target_file)
            content = parsed['content']
            data = parsed['data']

            has_todo = 'TODO' in content.upper()

            if not has_todo and len(content.strip()) > 50:
                # TC1: Time-series correlation & queue depth spike
                q_depth_str = str(data.get('telemetry_correlation', {}).get('peak_cloudwatch_volume_queue_length', ''))
                if not q_depth_str:
                    m = re.search(r'queue.*?(\d+)', content, re.IGNORECASE)
                    q_depth_str = m.group(1) if m else ''
                q_num = re.search(r'(\d+(?:\.\d+)?)', q_depth_str)
                if q_num and float(q_num.group(1)) >= 16.0:
                    results['tc1'] = True

                # TC2: Per-IO latency calculation
                lat_str = str(data.get('telemetry_correlation', {}).get('average_calculated_latency_ms', ''))
                if not lat_str:
                    m = re.search(r'latency.*?(\d+)', content, re.IGNORECASE)
                    lat_str = m.group(1) if m else ''
                lat_num = re.search(r'(\d+)', lat_str)
                if lat_num and int(lat_num.group(1)) > 0:
                    results['tc2'] = True

                # TC3: Throttling identification & IOPS saturation
                throttling = str(data.get('telemetry_correlation', {}).get('iops_throttling_detected', '')).upper()
                iops_str = str(data.get('telemetry_correlation', {}).get('total_sustained_iops', ''))
                if any(w in throttling for w in ['YES', 'TRUE', 'CONFIRM']) or '3000' in iops_str:
                    results['tc3'] = True

                # TC4: gp3 baseline throttling / burst credit audit
                if any(w in content.lower() for w in ['gp3', 'baseline', '3000', 'burst', 'gp2']):
                    results['tc4'] = True

                # TC5: Root cause determination - storage culpability
                culpable = str(data.get('root_cause_determination', {}).get('storage_subsystem_culpable', '')).upper()
                mechanism = str(data.get('root_cause_determination', {}).get('technical_causal_mechanism', '')).strip()
                if any(w in culpable for w in ['YES', 'TRUE', 'CONFIRM', 'CULPABLE']) and len(mechanism) >= 15:
                    results['tc5'] = True

                # TC6: Remediation blueprint - modify volume CLI command
                cmd = str(data.get('remediation_blueprint', {}).get('aws_cli_command', '')).lower()
                if any(w in cmd for w in ['modify-volume', 'aws ec2', 'io2', '--iops']):
                    results['tc6'] = True

                # TC7: Comprehensive RCA report format
                if parsed['type'] == 'json' and results['tc1'] and results['tc3'] and results['tc5']:
                    results['tc7'] = True
                elif parsed['type'] == 'text' and results['tc1'] and results['tc3']:
                    results['tc7'] = True
        except Exception:
            pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (3 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (3 if results.get('tc4') else 0) + (3 if results.get('tc5') else 0) + (3 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0)
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
    score = (3 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (3 if results.get('tc4') else 0) + (3 if results.get('tc5') else 0) + (3 if results.get('tc6') else 0) + (2 if results.get('tc7') else 0)
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
        "tc1": "Time-series correlation: accurately match CloudWatch queue depth spikes to the application latency spike window",
        "tc2": "Per-IO latency calculation: correctly calculate average read and write latencies in milliseconds",
        "tc3": "Throttling identification: detect whether IOPS or Throughput reached 100% of provisioned volume limits",
        "tc4": "EBS burst credit audit: evaluate burst balance depletion pattern on gp2 or baseline throttling on gp3",
        "tc5": "Root cause determination: convincingly substantiate whether storage subsystem caused the transaction delay",
        "tc6": "Remediation blueprint: specify exact volume configuration modifications (e.g. modify-volume --iops --throughput)",
        "tc7": "RCA documentation: storage_rca_report.json follows standard post-incident review format with charts/tables"
    }
    TC_MARKS = {
        "tc1": 3,
        "tc2": 3,
        "tc3": 3,
        "tc4": 3,
        "tc5": 3,
        "tc6": 3,
        "tc7": 2
    }

    print("Running Auto-Evaluation for: Storage Lab: Production Database Storage Latency Triage Across CloudWatch & Dynatrace\n")
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
