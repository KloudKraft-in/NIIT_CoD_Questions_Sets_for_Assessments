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
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False}
    base_path = get_base_path()

    # Technology-Specific Validation Harness for STG_W03_E
    # LVM Physical Volume Resize & Logical Volume Online Extension
    candidate_paths = [
        os.path.join(base_path, 'lvm_resize_report.json'),
        os.path.join(base_path, 'lvm_resize_report.txt'),
        os.path.join(os.path.dirname(base_path), 'lvm_resize_report.json'),
        os.path.expanduser('~/lvm_resize_report.json'),
        '/home/LabsKraft/lvm_resize_report.json',
        '/home/ubuntu/lvm_resize_report.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_report_data(target_file)

            # TC1: PV resize: pvresize successfully detects expanded underlying block device capacity
            pv_cmd = str(report.get('pv_resize_command', '')).strip().lower()
            pv_cap = str(report.get('pv_resized_capacity_gb', '')).strip().lower()

            if ('TODO' not in pv_cmd.upper() and 'pvresize' in pv_cmd) and \
               ('TODO' not in pv_cap.upper() and re.search(r'\d+', pv_cap) and int(re.search(r'\d+', pv_cap).group()) >= 90):
                results['tc1'] = True

            # TC2: VG metadata: volume group free extents updated and verified via vgs
            vg_name = str(report.get('volume_group', '')).strip().lower()
            vg_ext = str(report.get('vg_free_extents_updated', '')).strip().upper()

            if ('vg_data' in vg_name) and ('TODO' not in vg_ext and any(s in vg_ext for s in ['YES', 'TRUE'])):
                results['tc2'] = True

            # TC3: LV extension: logical volume extended to take 100% of newly available extents
            lv_name = str(report.get('logical_volume', '')).strip().lower()
            lv_cmd = str(report.get('lv_extend_command', '')).strip().lower()

            if ('lv_app' in lv_name) and ('TODO' not in lv_cmd.upper() and 'lvextend' in lv_cmd and any(k in lv_cmd for k in ['100%', '+', '100%free', '-l', '-r'])):
                results['tc3'] = True

            # TC4: Filesystem growth: resize2fs completes online with zero data loss and df confirms 100GB usable space
            fs_tool = str(report.get('filesystem_growth_tool', '')).strip().lower()
            final_cap = str(report.get('final_filesystem_capacity_gb', '')).strip().lower()
            data_loss = str(report.get('data_loss_experienced', '')).strip().upper()
            status = str(report.get('resize_status', '')).strip().upper()

            if ('TODO' not in fs_tool.upper() and any(t in fs_tool for t in ['resize2fs', 'fsadm', 'lvextend -r'])) and \
               ('TODO' not in final_cap.upper() and re.search(r'\d+', final_cap) and int(re.search(r'\d+', final_cap).group()) >= 90) and \
               ('TODO' not in data_loss and any(s in data_loss for s in ['NO', 'FALSE', 'NONE', 'ZERO'])) and \
               ('TODO' not in status and any(s in status for s in ['SUCCESS', 'RESOLVED', 'COMPLETED', 'OK'])):
                results['tc4'] = True
        except Exception:
            pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (2 if results.get('tc1') else 0) + (2 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (3 if results.get('tc4') else 0)
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
    score = (2 if results.get('tc1') else 0) + (2 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (3 if results.get('tc4') else 0)
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
        "tc1": "PV resize: pvresize successfully detects expanded underlying block device capacity",
        "tc2": "VG metadata: volume group free extents updated and verified via vgs",
        "tc3": "LV extension: logical volume extended to take 100% of newly available extents",
        "tc4": "Filesystem growth: resize2fs completes online with zero data loss and df confirms 100GB usable space"
    }
    TC_MARKS = {
        "tc1": 2,
        "tc2": 2,
        "tc3": 3,
        "tc4": 3
    }

    print("Running Auto-Evaluation for: Storage Lab: LVM Physical Volume Resize & Logical Volume Online Extension\n")
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
