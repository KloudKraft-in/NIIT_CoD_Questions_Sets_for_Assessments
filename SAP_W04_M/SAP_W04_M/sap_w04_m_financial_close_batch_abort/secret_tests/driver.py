import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    # Manual evaluation question - returns registered student deliverables state
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False}
    base_path = get_base_path()
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
    score = (5 if results.get('tc1') else 0) + (5 if results.get('tc2') else 0) + (5 if results.get('tc3') else 0) + (5 if results.get('tc4') else 0)
    total_marks = 20
    return score, total_marks, results

if __name__ == "__main__":
    results = run_tests()
    total_marks = 20
    TC_NAMES = {
        "tc1": "Correlation of canceled financial batch job in SM37 with ST22 dump",
        "tc2": "Forensic analysis of TSV_TNEW_PAGE_ALLOC_FAILED roll/extended/heap memory quotas",
        "tc3": "Idempotency validation verifying partial database commit state",
        "tc4": "Authoring compliant batch rerun change request with reduced packet size parameters"
}
    TC_MARKS = {
        "tc1": 5,
        "tc2": 5,
        "tc3": 5,
        "tc4": 5
}

    print("Manual Evaluation Question: SAP Basis Lab: Financial Close Batch Abort — SM37 Job Log & ST22 Memory Dump Forensic Remediation")
    print("[INFO] Deliverables submitted in student_workspace will be reviewed against the rubric:\n")
    for k, v in results.items():
        desc = TC_NAMES.get(k, '')
        marks = TC_MARKS.get(k, 0)
        status = "SUBMITTED" if v else "PENDING_REVIEW"
        print(f"{k.upper()} [{desc}]: {status} (Max: {marks} Marks)")
    print(f"\nMaximum Assessment Score: {total_marks} Marks")
    sys.exit(0)
