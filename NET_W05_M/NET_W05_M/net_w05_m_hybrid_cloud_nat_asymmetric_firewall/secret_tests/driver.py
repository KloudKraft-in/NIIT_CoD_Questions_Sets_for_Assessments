import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    # Manual evaluation question - checks presence of submitted triage deliverable
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False}
    base_path = get_base_path()
    sol_json = os.path.join(base_path, 'solution.json')
    triage_md = os.path.join(base_path, 'triage_report.md')

    # If student created triage_report.md with content, mark deliverables submitted
    has_report = os.path.exists(triage_md) and os.path.getsize(triage_md) > 100
    if has_report:
        for k in results.keys():
            results[k] = True

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

def verify_task_central(vm_tag, start_time, exam_code="UNKNOWN", **kwargs):
    results = run_tests()
    TC_MARKS = {
        "tc1": 5,
        "tc2": 5,
        "tc3": 5,
        "tc4": 5
}
    score = sum(TC_MARKS[k] for k, v in results.items() if v)
    total_marks = 20
    return score, total_marks, results

if __name__ == "__main__":
    results = run_tests()
    total_marks = 20
    TC_NAMES = {
        "tc1": "Comprehensive bidirectional path mapping between cloud VPC and on-premises datacenter",
        "tc2": "Accurate technical diagnosis of stateful firewall drops resulting from asymmetric routing",
        "tc3": "Evaluation of architectural remediation options (routing alignment vs NAT vs state bypass)",
        "tc4": "Formulation of a verified routing table modification and deployment plan"
}
    TC_MARKS = {
        "tc1": 5,
        "tc2": 5,
        "tc3": 5,
        "tc4": 5
}

    print("Manual Evaluation Question: Network Troubleshooting: Hybrid Cloud Asymmetric Routing & Stateful Firewall Drops")
    print("[INFO] Deliverables submitted in student_workspace will be reviewed against the rubric:\n")
    for k, v in results.items():
        desc = TC_NAMES.get(k, '')
        marks = TC_MARKS.get(k, 0)
        status = "SUBMITTED" if v else "PENDING_REVIEW"
        print(f"{k.upper()} [{desc}]: {status} (Max: {marks} Marks)")
    print(f"\nMaximum Assessment Score: {total_marks} Marks")
    sys.exit(0)
