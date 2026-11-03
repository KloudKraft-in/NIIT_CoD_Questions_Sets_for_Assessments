import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    # Manual evaluation question - checks presence of submitted triage deliverable
    results = {"tc1": False, "tc2": False, "tc3": False, "tc4": False, "tc5": False, "tc6": False, "tc7": False, "tc8": False}
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
        "tc1": 3,
        "tc2": 3,
        "tc3": 2,
        "tc4": 2,
        "tc5": 2,
        "tc6": 2,
        "tc7": 3,
        "tc8": 3
}
    score = sum(TC_MARKS[k] for k, v in results.items() if v)
    total_marks = 20
    return score, total_marks, results

if __name__ == "__main__":
    results = run_tests()
    total_marks = 20
    TC_NAMES = {
        "tc1": "Multi-layer forensic investigation integrating network, transport, and application telemetry",
        "tc2": "Accurate differentiation between root cause trigger and secondary cascade symptoms",
        "tc3": "Rigorous chronological timeline reconstruction of the major incident",
        "tc4": "Cross-system correlation of edge logs, connection tracking, and backend health status",
        "tc5": "Formulation of immediate operational stabilization and recovery procedures",
        "tc6": "Design of systemic architectural improvements to eliminate single points of failure",
        "tc7": "Development of early-warning observability metrics and synthetic health checks",
        "tc8": "Professional executive post-mortem and engineering corrective action plan"
}
    TC_MARKS = {
        "tc1": 3,
        "tc2": 3,
        "tc3": 2,
        "tc4": 2,
        "tc5": 2,
        "tc6": 2,
        "tc7": 3,
        "tc8": 3
}

    print("Manual Evaluation Question: Network Troubleshooting: Production Incident War-Room Multi-Layer Forensics")
    print("[INFO] Deliverables submitted in student_workspace will be reviewed against the rubric:\n")
    for k, v in results.items():
        desc = TC_NAMES.get(k, '')
        marks = TC_MARKS.get(k, 0)
        status = "SUBMITTED" if v else "PENDING_REVIEW"
        print(f"{k.upper()} [{desc}]: {status} (Max: {marks} Marks)")
    print(f"\nMaximum Assessment Score: {total_marks} Marks")
    sys.exit(0)
