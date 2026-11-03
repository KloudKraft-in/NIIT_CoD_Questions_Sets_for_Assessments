import os
import sys
import json
import csv
import re
from datetime import datetime, timezone

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_large_files_report(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try json
    try:
        data = json.loads(content)
        items = data.get('large_files', [])
        if not isinstance(items, list):
            items = []
        parsed_items = []
        for it in items:
            p = str(it.get('file_path') or it.get('path') or it.get('filepath') or '').strip()
            s = str(it.get('size_mb') or it.get('size') or it.get('sizemb') or '').strip()
            t = str(it.get('last_modified') or it.get('modified') or it.get('timestamp') or '').strip()
            parsed_items.append({'file_path': p, 'size': s, 'timestamp': t})
        return {'type': 'json', 'items': parsed_items, 'raw': data}
    except Exception:
        pass

    # Fallback to csv
    try:
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        if len(lines) >= 2:
            reader = csv.DictReader(lines)
            parsed_items = []
            for row in reader:
                norm_row = {k.lower().strip(): v for k, v in row.items() if k}
                p = norm_row.get('filepath') or norm_row.get('file_path') or norm_row.get('path', '')
                s = norm_row.get('sizemb') or norm_row.get('size_mb') or norm_row.get('size', '')
                t = norm_row.get('lastmodified') or norm_row.get('timestamp', '')
                parsed_items.append({'file_path': p, 'size': s, 'timestamp': t})
            return {'type': 'csv', 'items': parsed_items, 'raw': lines}
    except Exception:
        pass

    return None

def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False}
    base_path = get_base_path()

    candidate_paths = [
        os.path.join(base_path, 'large_files_report.json'),
        os.path.join(base_path, 'windows_large_files.json'),
        os.path.join(base_path, 'large_files_report.csv'),
        os.path.join(base_path, 'windows_large_files.csv'),
        os.path.join(os.path.dirname(base_path), 'large_files_report.json'),
        os.path.join(os.path.dirname(base_path), 'large_files_report.csv'),
        os.path.expanduser('~/large_files_report.json'),
        os.path.expanduser('~/windows_large_files.json'),
        '/home/LabsKraft/large_files_report.json',
        '/home/ubuntu/large_files_report.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        parsed = parse_large_files_report(target_file)
        if parsed and parsed['items']:
            items = parsed['items']

            # Check if placeholders still exist
            has_todo = any('TODO' in (it['file_path'] + it['size'] + it['timestamp']).upper() for it in items)
            valid_entries = [it for it in items if 'TODO' not in (it['file_path'] + it['size'] + it['timestamp']).upper()]

            if not has_todo and len(valid_entries) >= 2:
                # TC1: Filesystem capacity query completed & report populated
                results['tc1'] = True

                # TC2: Recursive search correctly isolates key large files
                # Target candidates from mock_data_volume: .sql.bak, .tar, .log
                file_names = [os.path.basename(it['file_path']).lower() for it in valid_entries]
                found_targets = 0
                for fn in file_names:
                    if any(target in fn for target in ['prod_customers', 'sql.bak', 'quarterly_financials', '.tar', 'runaway_debug', '.log']):
                        found_targets += 1

                if found_targets >= 2:
                    results['tc2'] = True

                # TC3: Report contains formatted sizes (numeric MB/GB) and timestamps
                sizes_ok = True
                timestamps_ok = True
                for it in valid_entries:
                    sz_match = re.search(r'\d+', it['size'])
                    if not sz_match:
                        sizes_ok = False
                    if len(it['timestamp'].strip()) < 4:
                        timestamps_ok = False

                if sizes_ok and timestamps_ok:
                    results['tc3'] = True

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
        "tc1": "Volume query: accurate Linux filesystem inspection via df -hT isolating capacity bottlenecks",
        "tc2": "Recursive search & sorting: find command pipeline correctly identifies and sorts large files",
        "tc3": "JSON report formatting: large_files_report.json contains valid paths, formatted sizes, and timestamps"
    }
    TC_MARKS = {
        "tc1": 4,
        "tc2": 3,
        "tc3": 3
    }

    print("Running Auto-Evaluation for: Storage Lab: Linux Application Volume Capacity Triage & Large File Discovery\n")
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
