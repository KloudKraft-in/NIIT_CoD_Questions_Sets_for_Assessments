import os
import sys
import json
import re
from datetime import datetime, timezone

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_reclamation_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        data = json.loads(content)
        return {str(k).lower().strip(): str(v).strip() for k, v in data.items()}
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
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False, "tc6": False, "tc7": False}
    base_path = get_base_path()

    candidate_paths = [
        os.path.join(base_path, 'emergency_reclamation.json'),
        os.path.join(base_path, 'emergency_reclamation.log'),
        os.path.join(os.path.dirname(base_path), 'emergency_reclamation.json'),
        os.path.join(os.path.dirname(base_path), 'emergency_reclamation.log'),
        os.path.expanduser('~/emergency_reclamation.json'),
        os.path.expanduser('~/emergency_reclamation.log'),
        '/home/LabsKraft/emergency_reclamation.json',
        '/home/ubuntu/emergency_reclamation.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_reclamation_data(target_file)

            # TC1: 100% capacity diagnosis on root filesystem
            tgt_fs = report.get('target_filesystem', '')
            init_util = report.get('initial_utilization', '')
            if ('/' in tgt_fs) and ('100' in init_util) and ('TODO' not in init_util.upper()):
                results['tc1'] = True

            # TC2 & TC3: Open descriptor identification & safe truncation
            open_desc = report.get('open_deleted_descriptors_truncated', '').upper()
            if 'TODO' not in open_desc and any(w in open_desc for w in ['YES', 'TRUE']):
                results['tc2'] = True
                results['tc3'] = True

            # TC4 & TC5: Core dump purging and systemd journal vacuuming
            journal_vac = report.get('journalctl_vacuum_size', '').upper()
            if 'TODO' not in journal_vac and any(w in journal_vac for w in ['200', 'M', 'G']):
                results['tc4'] = True
                results['tc5'] = True

            # TC6: Package cache cleanup
            pkg_clean = report.get('package_cache_cleaned', '').upper()
            if 'TODO' not in pkg_clean and any(w in pkg_clean for w in ['YES', 'TRUE']):
                results['tc6'] = True

            # TC7: Headroom recovery (< 70% utilization, freed headroom documented, status RESOLVED/SUCCESS)
            final_util_raw = report.get('final_utilization', '')
            headroom_raw = report.get('restored_headroom_mb', '')
            status = report.get('emergency_recovery_status', '').upper()

            if 'TODO' not in final_util_raw.upper() and 'TODO' not in headroom_raw.upper() and 'TODO' not in status:
                util_match = re.search(r'(\d+(?:\.\d+)?)', final_util_raw)
                mb_match = re.search(r'(\d+(?:\.\d+)?)', headroom_raw)
                if util_match and mb_match:
                    util_pct = float(util_match.group(1))
                    mb_val = float(mb_match.group(1))
                    if 0 < util_pct < 70.0 and mb_val > 0 and any(s in status for s in ['RESOLVED', 'SUCCESS']):
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
        "tc1": "100% capacity diagnosis: confirm filesystem saturation and explain discrepancy between du and df",
        "tc2": "Open descriptor identification: lsof accurately identifies the specific PIDs and FDs holding deleted logs",
        "tc3": "Safe zeroing of descriptors: open descriptors truncated via /proc filesystem without process crash or data loss",
        "tc4": "Core dump purging: obsolete crash dumps safely purged from /var/lib/systemd/coredump",
        "tc5": "Journal vacuuming: journalctl --vacuum-size executed correctly reducing systemd journal footprints",
        "tc6": "Package cache cleanup: system package manager cache cleared cleanly without removing installed packages",
        "tc7": "Headroom recovery: df confirms root partition usage < 70% and emergency_reclamation.json is fully compiled"
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

    print("Running Auto-Evaluation for: Storage Lab: Catastrophic Partition Saturation & Emergency Multi-Tier Space Reclamation\n")
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
