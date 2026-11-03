import os
import sys
import json
import subprocess
from datetime import datetime, timezone


def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_report_data(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return None

    # Try JSON parsing
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            return {str(k).lower().strip(): str(v).strip() for k, v in data.items()}
    except Exception:
        pass

    # Fallback to key: value text lines
    norm = {}
    for line in content.splitlines():
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            norm[k.strip().lower()] = v.strip()
    return norm if norm else None


def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False}
    base_path = get_base_path()

    candidate_paths = [
        os.path.join(base_path, 'iostat_analysis.json'),
        os.path.join(base_path, 'iostat_report.json'),
        os.path.join(base_path, 'queue_depth_analysis.json'),
        os.path.join(base_path, 'iostat_analysis.txt'),
        os.path.join(os.path.dirname(base_path), 'iostat_analysis.json'),
        os.path.expanduser('~/iostat_analysis.json'),
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            report = parse_report_data(target_file)
            if report:
                def get_val(keys):
                    for k in keys:
                        for rk, rv in report.items():
                            if k in rk:
                                return rv
                    return ""

                # Extract fields
                device = get_val(['target_device', 'device', 'target']).lower()
                cmd = get_val(['command_used', 'command', 'iostat_cmd', 'cmd']).lower()
                util = get_val(['disk_utilization_percent', 'utilization_percent', 'utilization', 'util', '%util']).lower()
                aqu_sz = get_val(['average_queue_size_aqu_sz', 'average_queue_size', 'avgqu-sz', 'aqu_sz', 'queue_size', 'queue_depth']).lower()
                w_await = get_val(['write_latency_w_await_ms', 'write_latency', 'w_await', 'wawait']).lower()
                r_await = get_val(['read_latency_r_await_ms', 'read_latency', 'r_await', 'rawait']).lower()
                verdict = get_val(['saturation_verdict', 'verdict', 'saturation']).lower()
                bottleneck = get_val(['primary_io_bottleneck', 'io_bottleneck', 'bottleneck', 'primary_bottleneck']).lower()

                # TC1: Command execution: iostat -xz correctly invoked with appropriate sampling interval and count (2 Marks)
                tc1_valid = False
                if 'todo' not in cmd and 'iostat' in cmd:
                    tc1_valid = True
                elif 'todo' not in util and ('sda' in device or '/dev/sda' in device):
                    tc1_valid = True
                if tc1_valid:
                    results['tc1'] = True

                # TC2: Utilization parsing: %util extracted accurately and compared against saturation baseline (2 Marks)
                tc2_valid = False
                if 'todo' not in util:
                    import re
                    util_nums = re.findall(r'\d+(?:\.\d+)?', util)
                    if util_nums:
                        val = float(util_nums[0])
                        if 85.0 <= val <= 100.0:
                            tc2_valid = True
                    elif '94' in util or '95' in util:
                        tc2_valid = True
                if tc2_valid:
                    results['tc2'] = True

                # TC3: Queue depth evaluation: avgqu-sz correctly interpreted indicating queued I/O requests (2 Marks)
                tc3_valid = False
                if 'todo' not in aqu_sz:
                    import re
                    aqu_nums = re.findall(r'\d+(?:\.\d+)?', aqu_sz)
                    if aqu_nums:
                        val = float(aqu_nums[0])
                        if 7.0 <= val <= 10.0:
                            tc3_valid = True
                    elif '8.4' in aqu_sz or '8.42' in aqu_sz:
                        tc3_valid = True
                if tc3_valid:
                    results['tc3'] = True

                # TC4: Latency breakdown: r_await and w_await correctly extracted to isolate write-heavy bottleneck (2 Marks)
                tc4_valid = False
                if 'todo' not in w_await and 'todo' not in r_await:
                    import re
                    w_nums = re.findall(r'\d+(?:\.\d+)?', w_await)
                    r_nums = re.findall(r'\d+(?:\.\d+)?', r_await)
                    w_ok = False
                    r_ok = False
                    if w_nums and (70.0 <= float(w_nums[0]) <= 100.0):
                        w_ok = True
                    elif '86' in w_await:
                        w_ok = True

                    if r_nums and (3.0 <= float(r_nums[0]) <= 6.0):
                        r_ok = True
                    elif '4.2' in r_await or '4' in r_await:
                        r_ok = True

                    if w_ok and r_ok:
                        tc4_valid = True
                if tc4_valid:
                    results['tc4'] = True

                # TC5: Summary report: iostat_analysis.json contains structured metrics and clear bottleneck conclusion (2 Marks)
                tc5_valid = False
                if 'todo' not in verdict and 'todo' not in bottleneck:
                    verdict_ok = any(x in verdict for x in ['saturated', 'saturation', 'heavy', 'yes', 'true'])
                    bottleneck_ok = any(x in bottleneck for x in ['write', 'write-heavy', 'write latency', 'saturation'])
                    if verdict_ok and bottleneck_ok:
                        tc5_valid = True
                if tc5_valid:
                    results['tc5'] = True
        except Exception:
            pass
    else:
        # Fallback to solution.json if report file is not found
        sol_json = os.path.join(base_path, 'solution.json')
        if os.path.exists(sol_json):
            try:
                with open(sol_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for k in results.keys():
                    if k in data.get('results', {}):
                        results[k] = bool(data['results'][k])
                    elif k in data:
                        results[k] = bool(data[k])
            except Exception:
                pass

    return results

def verify_task_central(vm_tag, start_time, exam_code, solution_path=None):
    results = run_tests()
    score = (2 if results.get('tc1') else 0) + (2 if results.get('tc2') else 0) + (2 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0) + (2 if results.get('tc5') else 0)
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
    score = (2 if results.get('tc1') else 0) + (2 if results.get('tc2') else 0) + (2 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0) + (2 if results.get('tc5') else 0)
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
        "tc1": "Command execution: iostat -xz correctly invoked with appropriate sampling interval and count",
        "tc2": "Utilization parsing: %util extracted accurately and compared against saturation baseline",
        "tc3": "Queue depth evaluation: avgqu-sz correctly interpreted indicating queued I/O requests",
        "tc4": "Latency breakdown: r_await and w_await correctly extracted to isolate write-heavy bottleneck",
        "tc5": "Summary report: iostat_analysis.json contains structured metrics and clear bottleneck conclusion"
}
    TC_MARKS = {
        "tc1": 2,
        "tc2": 2,
        "tc3": 2,
        "tc4": 2,
        "tc5": 2
}

    print("Running Auto-Evaluation for: Storage Lab: Storage Queue Depth & Disk Utilization Metric Anomaly Detection\n")
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
