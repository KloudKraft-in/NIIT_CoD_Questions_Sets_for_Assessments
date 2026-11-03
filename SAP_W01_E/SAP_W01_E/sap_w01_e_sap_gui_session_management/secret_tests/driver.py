import os
import sys
import json

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../student_workspace'))

def run_tests():
    # Manual evaluation question - returns registered student deliverables state
    results = {"tc1": False, "tc2": False, "tc3": False}
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
    score = (4 if results.get('tc1') else 0) + (3 if results.get('tc2') else 0) + (3 if results.get('tc3') else 0)
    total_marks = 10
    return score, total_marks, results

if __name__ == "__main__":
    results = run_tests()
    total_marks = 10
    TC_NAMES = {
        "tc1": "SAP Logon Pad configuration audit & message server SID validation",
        "tc2": "Logon group response-time load distribution check in SMLG",
        "tc3": "User session limits (rdisp/max_alt_modes) & hung desktop session triage"
}
    TC_MARKS = {
        "tc1": 4,
        "tc2": 3,
        "tc3": 3
}

    print("Manual Evaluation Question: SAP Basis Lab: SAP GUI Session Management & Logon Group Routing Verification")
    print("[INFO] Deliverables submitted in student_workspace will be reviewed against the rubric:\n")
    for k, v in results.items():
        desc = TC_NAMES.get(k, '')
        marks = TC_MARKS.get(k, 0)
        status = "SUBMITTED" if v else "PENDING_REVIEW"
        print(f"{k.upper()} [{desc}]: {status} (Max: {marks} Marks)")
    print(f"\nMaximum Assessment Score: {total_marks} Marks")
    sys.exit(0)
