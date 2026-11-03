import os
import sys
import re
import json
import subprocess
from datetime import datetime, timezone


def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False}
    base_path = get_base_path()
    sol_json = os.path.join(base_path, 'solution.json')
    
    # 1. Parse student solution payload if provided
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

    # 2. Technology-Specific Validation Harness
    # Storage Performance Verification Logic
    # Locate perf_diagnosis.json (check .json first, fallback to .txt)
    diagnosis_paths = [
        os.path.join(base_path, 'perf_diagnosis.json'),
        os.path.join(base_path, 'perf_diagnosis.txt'),
        os.path.join(os.path.dirname(base_path), 'perf_diagnosis.json'),
        os.path.join(os.path.dirname(base_path), 'perf_diagnosis.txt'),
        os.path.expanduser('~/perf_diagnosis.json'),
        os.path.expanduser('~/perf_diagnosis.txt'),
        '/home/LabsKraft/perf_diagnosis.json',
        '/home/LabsKraft/perf_diagnosis.txt',
        '/home/ubuntu/perf_diagnosis.json',
        '/home/ubuntu/perf_diagnosis.txt',
    ]
    perf_file = None
    for p in diagnosis_paths:
        if os.path.isfile(p):
            perf_file = p
            break

    # Locate fio_summary.log
    fio_paths = [
        os.path.join(base_path, 'fio_summary.log'),
        os.path.join(os.path.dirname(base_path), 'fio_summary.log'),
        '/opt/storage_bench/fio_summary.log',
        os.path.expanduser('~/fio_summary.log'),
        '/home/LabsKraft/fio_summary.log',
        '/home/ubuntu/fio_summary.log',
    ]
    fio_file = None
    for p in fio_paths:
        if os.path.isfile(p):
            fio_file = p
            break

    perf_content = ""
    perf_data = {}
    if perf_file:
        try:
            with open(perf_file, 'r', encoding='utf-8', errors='ignore') as f:
                perf_content = f.read()
            if perf_file.endswith('.json'):
                try:
                    perf_data = json.loads(perf_content)
                except Exception:
                    perf_data = {}
        except Exception:
            perf_content = ""

    norm_dict = {str(k).lower().strip(): v for k, v in perf_data.items()} if isinstance(perf_data, dict) else {}

    # TC1: Log inspection - successfully parse IOPS, completion latency, and transfer rates from fio_summary.log
    fio_exists = fio_file is not None or os.path.exists(os.path.join(base_path, 'fio_summary.log'))
    has_diagnostic_data = False
    if norm_dict:
        todos = [v for v in norm_dict.values() if isinstance(v, str) and 'TODO' in v.upper()]
        if len(todos) < len(norm_dict) and len(norm_dict) >= 3:
            has_diagnostic_data = True
    elif perf_content:
        # Check if placeholders were replaced in text format
        todos = [t for t in ['TODO_CALCULATE', 'TODO_BOTTLENECK', 'TODO_SUMMARY'] if t in perf_content]
        if len(todos) < 3:
            has_diagnostic_data = True

    has_inspection_script = False
    try:
        for fname in os.listdir(base_path):
            fpath = os.path.join(base_path, fname)
            if fname.endswith(('.py', '.sh', '.json', '.log')) and fname not in ['run.py', 'solution.json', 'fio_summary.log', 'perf_diagnosis.json']:
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        fc = f.read()
                    if any(term in fc.lower() for term in ['iops', 'latency', 'clat', '4096', '256k', '58.6', '500']):
                        has_inspection_script = True
                        break
                except Exception:
                    pass
    except Exception:
        pass

    if fio_exists and (has_diagnostic_data or has_inspection_script):
        results['tc1'] = True
    elif os.path.exists('/proc/mounts') and has_diagnostic_data:
        results['tc1'] = True

    # TC2: Metric calculation - accurate computation of theoretical vs measured throughput across different block sizes
    # Formula: Throughput (MB/s) = (IOPS * Block Size in KB) / 1024
    # 4KB profile: 15000 * 4 / 1024 = 58.59 MB/s (~58.6 MB/s, measured 58.6 MiB/s / 61.4 MB/s)
    # 256KB profile: 2000 * 256 / 1024 = 500.0 MB/s (measured 500 MiB/s / 524 MB/s)
    calc_4kb_ok = False
    calc_256kb_ok = False

    if norm_dict:
        v4 = norm_dict.get('throughput_4kb_mbps', norm_dict.get('throughput_4kb', norm_dict.get('4kb')))
        if v4 is not None and not (isinstance(v4, str) and 'TODO' in v4.upper()):
            nums = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', str(v4))]
            if any(50.0 <= n <= 65.0 for n in nums):
                calc_4kb_ok = True

        v256 = norm_dict.get('throughput_256kb_mbps', norm_dict.get('throughput_256kb', norm_dict.get('256kb')))
        if v256 is not None and not (isinstance(v256, str) and 'TODO' in v256.upper()):
            nums = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', str(v256))]
            if any(480.0 <= n <= 535.0 for n in nums):
                calc_256kb_ok = True

    if (not calc_4kb_ok or not calc_256kb_ok) and perf_content:
        m4 = re.search(r'THROUGHPUT_4KB(?:_MBPS)?\s*:\s*([^\r\n#]+)', perf_content, re.IGNORECASE)
        if m4 and 'TODO' not in m4.group(1).upper():
            val_str = m4.group(1).strip()
            nums = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', val_str)]
            if any(50.0 <= n <= 65.0 for n in nums):
                calc_4kb_ok = True

        m256 = re.search(r'THROUGHPUT_256KB(?:_MBPS)?\s*:\s*([^\r\n#]+)', perf_content, re.IGNORECASE)
        if m256 and 'TODO' not in m256.group(1).upper():
            val_str = m256.group(1).strip()
            nums = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', val_str)]
            if any(480.0 <= n <= 535.0 for n in nums):
                calc_256kb_ok = True

    # Check other json files if student saved metrics there
    if not (calc_4kb_ok and calc_256kb_ok):
        try:
            for fname in os.listdir(base_path):
                if fname.endswith('.json') and fname not in ['solution.json', 'perf_diagnosis.json']:
                    with open(os.path.join(base_path, fname), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    flat_text = json.dumps(data)
                    if 'TODO' not in flat_text.upper():
                        nums = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', flat_text)]
                        if any(50.0 <= n <= 65.0 for n in nums):
                            calc_4kb_ok = True
                        if any(480.0 <= n <= 535.0 for n in nums):
                            calc_256kb_ok = True
        except Exception:
            pass

    # TC3: Bottleneck diagnosis - correctly identifies IOPS throttling due to small 4KB random reads
    bottleneck_identified = False
    rationale_valid = False

    if norm_dict:
        vb = norm_dict.get('identified_bottleneck', norm_dict.get('bottleneck'))
        if vb and not (isinstance(vb, str) and 'TODO' in vb.upper()):
            clean_b = str(vb).strip('[] ').lower()
            if 'iops' in clean_b and 'throughput' not in clean_b and 'latency' not in clean_b:
                bottleneck_identified = True

        vs = norm_dict.get('diagnosis_summary', norm_dict.get('summary', norm_dict.get('diagnosis')))
        if vs and not (isinstance(vs, str) and 'TODO' in vs.upper()):
            sum_str = str(vs).strip().lower()
            if len(sum_str) >= 20:
                has_iops = any(k in sum_str for k in ['iops', 'operation', 'io '])
                has_limit = any(k in sum_str for k in ['throttl', 'limit', 'bound', 'saturat', 'cap', 'exceed', 'hit', 'bottleneck', 'max', 'reach'])
                if has_iops and has_limit:
                    rationale_valid = True

    if (not bottleneck_identified or not rationale_valid) and perf_content:
        mb = re.search(r'IDENTIFIED_BOTTLENECK\s*:\s*([^\r\n#]+)', perf_content, re.IGNORECASE)
        if mb and 'TODO' not in mb.group(1).upper():
            clean_b = mb.group(1).strip('[] ').lower()
            if 'iops' in clean_b and 'throughput' not in clean_b and 'latency' not in clean_b:
                bottleneck_identified = True

        ms = re.search(r'DIAGNOSIS_SUMMARY\s*:\s*([^\r\n]+(?:\n(?![A-Z0-9_]+:)[^\r\n]+)*)', perf_content, re.IGNORECASE)
        if ms and 'TODO' not in ms.group(1).upper():
            sum_str = ms.group(1).strip().lower()
            if len(sum_str) >= 20:
                has_iops = any(k in sum_str for k in ['iops', 'operation', 'io '])
                has_limit = any(k in sum_str for k in ['throttl', 'limit', 'bound', 'saturat', 'cap', 'exceed', 'hit', 'bottleneck', 'max', 'reach'])
                if has_iops and has_limit:
                    rationale_valid = True

    results['tc1'] = bool(fio_exists and (has_diagnostic_data or has_inspection_script))
    results['tc2'] = bool(calc_4kb_ok and calc_256kb_ok)
    results['tc3'] = bool(bottleneck_identified and rationale_valid)

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
        "tc1": "Log inspection: successfully parse IOPS, average completion latency, and transfer rates from fio_summary.log",
        "tc2": "Metric calculation: accurate computation of theoretical vs measured throughput across different block size profiles",
        "tc3": "Bottleneck diagnosis: perf_diagnosis.json correctly identifies IOPS throttling due to small 4KB random reads"
}
    TC_MARKS = {
        "tc1": 4,
        "tc2": 3,
        "tc3": 3
}

    print("Running Auto-Evaluation for: Storage Lab: Storage Performance Metrics — IOPS, Throughput & Latency Dissection\n")
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
