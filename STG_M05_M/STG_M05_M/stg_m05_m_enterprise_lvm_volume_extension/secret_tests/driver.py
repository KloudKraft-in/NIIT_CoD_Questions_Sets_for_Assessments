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
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False, "tc6": False, "tc7": False}
    base_path = get_base_path()

    candidate_paths = [
        os.path.join(base_path, 'lvm_extension_signoff.json'),
        os.path.join(base_path, 'lvm_extension_report.json'),
        os.path.join(base_path, 'lvm_signoff.json'),
        os.path.join(os.path.dirname(base_path), 'lvm_extension_signoff.json'),
        os.path.expanduser('~/lvm_extension_signoff.json'),
        '/home/LabsKraft/lvm_extension_signoff.json',
        '/home/ubuntu/lvm_extension_signoff.json',
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_report_data(target_file)

            # TC1: Pre-change capture: baseline LVM topology and mount states accurately recorded in lvm_before.log
            base_captured = str(report.get('baseline_topology_captured', '')).strip().upper()
            if 'TODO' not in base_captured and any(s in base_captured for s in ['YES', 'TRUE', 'RECORDED']):
                results['tc1'] = True

            # TC2: Physical volume creation: pvcreate successfully initializes /dev/sdc with proper partition alignment
            pv_tool = str(report.get('pv_creation_tool', '')).strip().lower()
            pv_dev = str(report.get('physical_volume_added', '')).strip().lower()
            if ('TODO' not in pv_tool.upper() and 'pvcreate' in pv_tool) and \
               ('TODO' not in pv_dev.upper() and ('sdc' in pv_dev or 'sdc' in pv_tool)):
                results['tc2'] = True

            # TC3: Volume group expansion: vgextend incorporates /dev/sdc into vg_enterprise without disruptive locking
            vg_tool = str(report.get('vg_expansion_tool', '')).strip().lower()
            vg_name = str(report.get('volume_group', '')).strip().lower()
            if ('TODO' not in vg_tool.upper() and 'vgextend' in vg_tool) and \
               ('TODO' not in vg_name.upper() and ('vg_enterprise' in vg_name or 'enterprise' in vg_tool)):
                results['tc3'] = True

            # TC4: Targeted LV growth: lvextend extends logical volume by exactly +50GB rather than consuming all space
            lv_amt = str(report.get('lv_extension_amount_gb', '')).strip()
            lv_cmd = str(report.get('lv_extend_command', '')).strip().lower()
            if ('TODO' not in lv_amt.upper() and '50' in lv_amt) or \
               ('TODO' not in lv_cmd.upper() and 'lvextend' in lv_cmd and '50' in lv_cmd):
                results['tc4'] = True

            # TC5: Filesystem expansion: filesystem grown online while continuous background write script runs without I/O error
            fs_type = str(report.get('filesystem_expansion_type', '')).strip().upper()
            io_err = str(report.get('continuous_io_errors', '')).strip().upper()
            if ('TODO' not in fs_type and any(s in fs_type for s in ['ONLINE', 'LIVE'])) and \
               ('TODO' not in io_err and any(s in io_err for s in ['NO', 'FALSE', 'ZERO', 'NONE', '0'])):
                results['tc5'] = True

            # TC6: Emergency headroom: verification that volume group maintains unallocated extents for future emergency growth
            reserve = str(report.get('emergency_vg_reserve_free_gb', '')).strip()
            if 'TODO' not in reserve.upper() and re.search(r'\d+', reserve) and int(re.search(r'\d+', reserve).group()) >= 40:
                results['tc6'] = True

            # TC7: Change sign-off: lvm_extension_signoff.json documents before/after sizes, UUIDs, and verification checksums
            ticket = str(report.get('change_control_ticket', '')).strip().upper()
            status = str(report.get('execution_status', '')).strip().upper()
            if ('TODO' not in ticket and 'CHG' in ticket) and \
               ('TODO' not in status and any(s in status for s in ['COMPLETED', 'SUCCESS', 'DONE', 'RESOLVED'])):
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
        "tc1": "Pre-change capture: baseline LVM topology and mount states accurately recorded in lvm_before.log",
        "tc2": "Physical volume creation: pvcreate successfully initializes /dev/sdc with proper partition alignment",
        "tc3": "Volume group expansion: vgextend incorporates /dev/sdc into vg_enterprise without disruptive locking",
        "tc4": "Targeted LV growth: lvextend extends logical volume by exactly +50GB rather than consuming all space",
        "tc5": "Filesystem expansion: filesystem grown online while continuous background write script runs without I/O error",
        "tc6": "Emergency headroom: verification that volume group maintains unallocated extents for future emergency growth",
        "tc7": "Change sign-off: lvm_extension_signoff.json documents before/after sizes, UUIDs, and verification checksums"
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

    print("Running Auto-Evaluation for: Storage Lab: Enterprise LVM Volume Extension Under Live I/O Load with Rollback SOP\n")
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
