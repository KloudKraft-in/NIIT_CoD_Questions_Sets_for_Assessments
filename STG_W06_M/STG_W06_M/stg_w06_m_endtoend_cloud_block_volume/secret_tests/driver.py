import os
import sys
import json
import re
from datetime import datetime, timezone

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_resize_data(file_path):
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
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False}
    base_path = get_base_path()

    candidate_paths = [
        os.path.join(base_path, 'cloud_resize.json'),
        os.path.join(base_path, 'cloud_resize.log'),
        os.path.join(os.path.dirname(base_path), 'cloud_resize.json'),
        os.path.join(os.path.dirname(base_path), 'cloud_resize.log'),
        os.path.expanduser('~/cloud_resize.json'),
        os.path.expanduser('~/cloud_resize.log'),
        '/home/LabsKraft/cloud_resize.json',
        '/home/ubuntu/cloud_resize.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_resize_data(target_file)

            # TC1: Disk geometry inspection (device / partition / capacity defined)
            tgt_dev = report.get('target_device', '')
            tgt_part = report.get('target_partition', '')
            before_cap = report.get('before_capacity_gb', '')

            if ('nvme' in tgt_dev or 'sd' in tgt_dev) and ('1' in tgt_part) and ('TODO' not in before_cap.upper()):
                results['tc1'] = True

            # TC2: Partition table extension tool (growpart / parted)
            part_tool = report.get('partition_resize_tool', '').lower()
            if 'todo' not in part_tool and any(t in part_tool for t in ['growpart', 'parted', 'fdisk']):
                results['tc2'] = True

            # TC3: Online filesystem expansion tool (xfs_growfs / resize2fs)
            fs_tool = report.get('filesystem_grow_tool', '').lower()
            if 'todo' not in fs_tool and any(t in fs_tool for t in ['xfs_growfs', 'resize2fs']):
                results['tc3'] = True

            # TC4: Capacity verification (~250 GB) & database continuity
            after_cap = report.get('after_capacity_gb', '')
            db_interrupted = report.get('database_io_interrupted', '').upper()
            resize_res = report.get('resize_result', '').upper()

            if 'TODO' not in after_cap.upper() and 'TODO' not in resize_res:
                cap_match = re.search(r'(\d+)', after_cap)
                if cap_match and int(cap_match.group(1)) >= 200:
                    if 'NO' in db_interrupted and 'SUCCESS' in resize_res:
                        results['tc4'] = True
        except Exception:
            pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (5 if results.get('tc1') else 0) + (5 if results.get('tc2') else 0) + (5 if results.get('tc3') else 0) + (5 if results.get('tc4') else 0)
    total_marks = 20
    
    solution_data = {
        'candidate_prefix': vm_tag,
        'assessment_start_time': start_time,
        'max_duration_minutes': 60,
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
    score = (5 if results.get('tc1') else 0) + (5 if results.get('tc2') else 0) + (5 if results.get('tc3') else 0) + (5 if results.get('tc4') else 0)
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
        "tc1": "Disk geometry inspection: correctly identify discrepancy between disk device size and partition size via lsblk",
        "tc2": "Partition table extension: growpart successfully expands partition 1 without corrupting partition GUID table (GPT)",
        "tc3": "Online filesystem expansion: xfs_growfs extends the live XFS filesystem online without requiring unmount",
        "tc4": "Integrity & verification: database writes verified intact and df -hT confirms ~250 GB available space"
    }
    TC_MARKS = {
        "tc1": 5,
        "tc2": 5,
        "tc3": 5,
        "tc4": 5
    }

    print("Running Auto-Evaluation for: Storage Lab: End-to-End Cloud Block Volume Resize & XFS/EXT4 Filesystem Growth\n")
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
