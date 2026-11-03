import os
import sys
import json
import subprocess
from datetime import datetime, timezone


def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def parse_tier_mappings(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return None

    data = None
    try:
        data = json.loads(content)
    except Exception:
        pass

    normalized = {}

    def extract_entry(item):
        wl_id = None
        for key in ['workload_id', 'id', 'workload', 'wl_id', 'name']:
            if key in item and isinstance(item[key], str):
                val = item[key].strip().upper()
                if 'WL-01' in val or 'WL01' in val or 'WL-1' in val or val == '1':
                    wl_id = 'WL-01'
                elif 'WL-02' in val or 'WL02' in val or 'WL-2' in val or val == '2':
                    wl_id = 'WL-02'
                elif 'WL-03' in val or 'WL03' in val or 'WL-3' in val or val == '3':
                    wl_id = 'WL-03'
                elif 'WL-04' in val or 'WL04' in val or 'WL-4' in val or val == '4':
                    wl_id = 'WL-04'
                break

        aws_val = ""
        azure_val = ""
        gcp_val = ""
        for k, v in item.items():
            if not isinstance(v, str):
                continue
            k_low = k.lower()
            if 'aws' in k_low or 'amazon' in k_low:
                aws_val = v.strip().lower()
            elif 'azure' in k_low or 'ms' in k_low:
                azure_val = v.strip().lower()
            elif 'gcp' in k_low or 'google' in k_low:
                gcp_val = v.strip().lower()

        return wl_id, {'aws': aws_val, 'azure': azure_val, 'gcp': gcp_val}

    if isinstance(data, dict):
        list_key = None
        for k in ['tier_mappings', 'mappings', 'workloads', 'tiers', 'workload_profiles']:
            if k in data and isinstance(data[k], list):
                list_key = k
                break

        if list_key:
            for item in data[list_key]:
                if isinstance(item, dict):
                    wid, tiers = extract_entry(item)
                    if wid:
                        normalized[wid] = tiers
        else:
            for k, v in data.items():
                if isinstance(v, dict):
                    k_upper = str(k).strip().upper()
                    wid = None
                    if 'WL-01' in k_upper or 'WL01' in k_upper or k_upper == '1':
                        wid = 'WL-01'
                    elif 'WL-02' in k_upper or 'WL02' in k_upper or k_upper == '2':
                        wid = 'WL-02'
                    elif 'WL-03' in k_upper or 'WL03' in k_upper or k_upper == '3':
                        wid = 'WL-03'
                    elif 'WL-04' in k_upper or 'WL04' in k_upper or k_upper == '4':
                        wid = 'WL-04'

                    if wid:
                        _, tiers = extract_entry(v)
                        normalized[wid] = tiers
                    else:
                        item_wid, tiers = extract_entry(v)
                        if item_wid:
                            normalized[item_wid] = tiers
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                wid, tiers = extract_entry(item)
                if wid:
                    normalized[wid] = tiers

    return normalized


def run_tests():
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False}
    base_path = get_base_path()

    candidate_paths = [
        os.path.join(base_path, 'cloud_storage_tiers.json'),
        os.path.join(base_path, 'storage_tiers.json'),
        os.path.join(base_path, 'tier_mappings.json'),
        os.path.join(base_path, 'cloud_tiers.json'),
        os.path.join(os.path.dirname(base_path), 'cloud_storage_tiers.json'),
        os.path.expanduser('~/cloud_storage_tiers.json'),
    ]

    target_file = None
    for cp in candidate_paths:
        if os.path.exists(cp):
            target_file = cp
            break

    if target_file:
        try:
            tiers_map = parse_tier_mappings(target_file)
            if tiers_map:
                # TC1: High-IOPS database mapping: correctly select AWS io2, Azure Ultra Disk, and GCP pd-extreme
                wl1 = tiers_map.get('WL-01')
                if wl1:
                    aws = wl1.get('aws', '')
                    azure = wl1.get('azure', '')
                    gcp = wl1.get('gcp', '')
                    if aws and azure and gcp and ('todo' not in aws) and ('todo' not in azure) and ('todo' not in gcp):
                        aws_ok = any(x in aws for x in ['io2', 'io1', 'block express', 'provisioned iops'])
                        azure_ok = any(x in azure for x in ['ultra', 'premium ssd v2', 'v2', 'ultra disk'])
                        gcp_ok = any(x in gcp for x in ['extreme', 'pd-extreme', 'hyperdisk'])
                        if aws_ok and azure_ok and gcp_ok:
                            results['tc1'] = True

                # TC2: General purpose workload mapping: select AWS gp3, Azure Premium SSD, and GCP pd-balanced
                wl2 = tiers_map.get('WL-02')
                if wl2:
                    aws = wl2.get('aws', '')
                    azure = wl2.get('azure', '')
                    gcp = wl2.get('gcp', '')
                    if aws and azure and gcp and ('todo' not in aws) and ('todo' not in azure) and ('todo' not in gcp):
                        aws_ok = any(x in aws for x in ['gp3', 'gp2', 'general purpose'])
                        azure_ok = any(x in azure for x in ['premium ssd', 'premium', 'standard ssd'])
                        gcp_ok = any(x in gcp for x in ['balanced', 'pd-balanced', 'standard', 'pd-standard'])
                        if aws_ok and azure_ok and gcp_ok:
                            results['tc2'] = True

                # TC3: Throughput-optimized workload mapping: select AWS st1 / io2, Azure Premium SSD v2, and GCP pd-ssd
                wl3 = tiers_map.get('WL-03')
                if wl3:
                    aws = wl3.get('aws', '')
                    azure = wl3.get('azure', '')
                    gcp = wl3.get('gcp', '')
                    if aws and azure and gcp and ('todo' not in aws) and ('todo' not in azure) and ('todo' not in gcp):
                        aws_ok = any(x in aws for x in ['st1', 'throughput', 'io2', 'sc1'])
                        azure_ok = any(x in azure for x in ['v2', 'premium ssd v2', 'ultra', 'premium'])
                        gcp_ok = any(x in gcp for x in ['pd-ssd', 'ssd', 'throughput', 'hyperdisk', 'extreme'])
                        if aws_ok and azure_ok and gcp_ok:
                            results['tc3'] = True

                # TC4: Archive tier mapping: select appropriate deep cold object storage tiers across all 3 providers
                wl4 = tiers_map.get('WL-04')
                if wl4:
                    aws = wl4.get('aws', '')
                    azure = wl4.get('azure', '')
                    gcp = wl4.get('gcp', '')
                    if aws and azure and gcp and ('todo' not in aws) and ('todo' not in azure) and ('todo' not in gcp):
                        aws_ok = any(x in aws for x in ['glacier', 'deep archive', 'archive'])
                        azure_ok = any(x in azure for x in ['archive', 'blob archive', 'blob'])
                        gcp_ok = any(x in gcp for x in ['archive', 'cloud storage archive', 'coldline'])
                        if aws_ok and azure_ok and gcp_ok:
                            results['tc4'] = True
        except Exception:
            pass
    else:
        # Fallback to solution.json if target file is completely missing
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
    score = (3 if results.get('tc1') else 0) + (2 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0)
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
    score = (3 if results.get('tc1') else 0) + (2 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0) + (2 if results.get('tc4') else 0)
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
        "tc1": "High-IOPS database mapping: correctly select AWS io2, Azure Ultra Disk, and GCP pd-extreme",
        "tc2": "General purpose workload mapping: select AWS gp3, Azure Premium SSD, and GCP pd-balanced",
        "tc3": "Throughput-optimized workload mapping: select AWS st1 / io2, Azure Premium SSD v2, and GCP pd-ssd",
        "tc4": "Archive tier mapping: select appropriate deep cold object storage tiers across all 3 providers"
}
    TC_MARKS = {
        "tc1": 3,
        "tc2": 2,
        "tc3": 3,
        "tc4": 2
}

    print("Running Auto-Evaluation for: Storage Lab: Cross-Cloud Storage Architecture & Performance Tier Selection\n")
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
