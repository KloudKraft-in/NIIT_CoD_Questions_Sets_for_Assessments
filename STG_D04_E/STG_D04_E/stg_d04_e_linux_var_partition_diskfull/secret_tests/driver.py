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

    # Try json first
    try:
        data = json.loads(content)
        # Normalize keys to lowercase
        norm = {str(k).lower().strip(): v for k, v in data.items()}
        return norm
    except Exception:
        pass

    # Fallback to key: value text lines
    norm = {}
    for line in content.splitlines():
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            norm[k.strip().lower()] = v.strip()
    return norm

def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False}
    base_path = get_base_path()

    # Technology-Specific Validation Harness for STG_D04_E
    # Linux /var Partition Disk-Full SOP Execution & Safe Log Cleanup
    candidate_paths = [
        os.path.join(base_path, 'cleanup_report.json'),
        os.path.join(base_path, 'cleanup_report.txt'),
        os.path.join(os.path.dirname(base_path), 'cleanup_report.json'),
        os.path.join(os.path.dirname(base_path), 'cleanup_report.txt'),
        os.path.expanduser('~/cleanup_report.json'),
        os.path.expanduser('~/cleanup_report.txt'),
        '/home/LabsKraft/cleanup_report.json',
        '/home/LabsKraft/cleanup_report.txt',
        '/home/ubuntu/cleanup_report.json',
        '/home/ubuntu/cleanup_report.txt',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_report_data(target_file)

            # TC1: Target partition is /var and recovery status is SUCCESS
            target_part = str(report.get('target_partition', '')).strip()
            recovery_stat = str(report.get('recovery_status', '')).strip().upper()
            init_usage = str(report.get('initial_usage_percent', '')).strip()

            if ('/var' in target_part) and ('TODO' not in recovery_stat and any(s in recovery_stat for s in ['SUCCESS', 'RESOLVED'])) and ('TODO' not in init_usage.upper()):
                results['tc1'] = True

            # TC2: Safe cleanup applied and active file descriptors preserved
            safe_clean = str(report.get('safe_log_cleanup_applied', '')).strip().upper()
            active_fd = str(report.get('active_file_descriptors_preserved', '')).strip().upper()

            if ('TODO' not in safe_clean and any(s in safe_clean for s in ['YES', 'TRUE'])) and \
               ('TODO' not in active_fd and any(s in active_fd for s in ['YES', 'TRUE'])):
                results['tc2'] = True

            # TC3: Final usage percent is < 75% and freed megabytes is quantified
            final_usage_raw = str(report.get('final_usage_percent', '')).strip()
            freed_mb_raw = str(report.get('freed_megabytes', '')).strip()

            if 'TODO' not in final_usage_raw.upper() and 'TODO' not in freed_mb_raw.upper():
                # Extract numeric values
                final_pct_match = re.search(r'(\d+(?:\.\d+)?)', final_usage_raw)
                freed_mb_match = re.search(r'(\d+(?:\.\d+)?)', freed_mb_raw)

                if final_pct_match and freed_mb_match:
                    final_pct = float(final_pct_match.group(1))
                    freed_mb = float(freed_mb_match.group(1))
                    if 0 < final_pct < 75.0 and freed_mb > 0:
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
        "tc1": "Identification of space hogs: script or command output correctly isolates the specific offending log directories",
        "tc2": "Safe cleanup execution: historical archives compressed/purged while active process file descriptors remain undamaged",
        "tc3": "Threshold recovery: verify /var partition utilization is below 75% and cleanup_report.json documents exact freed bytes"
    }
    TC_MARKS = {
        "tc1": 4,
        "tc2": 3,
        "tc3": 3
    }

    print("Running Auto-Evaluation for: Storage Lab: Linux /var Partition Disk-Full SOP Execution & Safe Log Cleanup\n")
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
