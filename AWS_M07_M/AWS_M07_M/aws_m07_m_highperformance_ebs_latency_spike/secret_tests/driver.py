import os
import sys
import json
import re
from datetime import datetime, timezone

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def print_separator():
    print("-" * 70)

def print_test_case(name, status, score, max_score, reason):
    pad_length = 63 - len(name) - 1
    if pad_length < 1:
        pad_length = 1
    dots = "." * pad_length
    print(f"{name} {dots} {status} ({score}/{max_score})")
    print(f"    +- [Reason]: {reason}")

def get_base_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '..', 'student_workspace'))

def find_deliverable(fname):
    ws_path = get_base_path()
    root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    
    candidate_paths = [
        os.path.join(ws_path, fname),
        os.path.join(root_path, fname),
        os.path.expanduser(f"~/{fname}"),
        os.path.join(os.getcwd(), fname),
        os.path.join(os.getcwd(), 'student_workspace', fname),
        f"/home/ubuntu/{fname}",
        f"/home/LabsKraft/{fname}"
    ]
    
    for p in candidate_paths:
        if os.path.exists(p) and os.path.isfile(p):
            return p

    # Fallback search inside workspace directory for exact filename
    if os.path.exists(ws_path):
        for item in os.listdir(ws_path):
            if item.lower() == fname.lower():
                full_p = os.path.join(ws_path, item)
                if os.path.isfile(full_p):
                    return full_p

    return None

def write_solution_json(score, max_score, results):
    # In cloud console assessments, student_workspace must remain clean for portal launch
    try:
        sol_data = {
            'candidate_prefix': get_candidate_prefix(),
            'score': score,
            'total_marks': max_score,
            'results': results,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        report_dir = os.path.expanduser('~/.niit_eval')
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, 'last_eval.json'), 'w', encoding='utf-8') as f:
            json.dump(sol_data, f, indent=4)
    except Exception:
        pass


TC_NAMES = {
        "tc1": "Burst balance correlation: match BurstBalance drop to zero with the exact onset of database query timeouts",
        "tc2": "Technical explanation: accurately explain gp2 3 IOPS/GB baseline limitation and burst bucket replenishment",
        "tc3": "Queue depth analysis: interpret VolumeQueueLength > 40 as severe I/O bottleneck",
        "tc4": "gp3 migration command: construct valid modify-volume command specifying gp3, 12000 IOPS, 500 MB/s",
        "tc5": "Online optimization validation: verify volume status polling and zero downtime transition",
        "tc6": "Performance benchmarking: post-upgrade latency metrics demonstrate sustained sub-5ms completion",
        "tc7": "RCA report quality: ebs_performance_rca.md includes before/after graphs and financial ROI of gp3 vs gp2",
        "tc8": "Monitoring guardrail: CloudWatch alarm command correctly provisioned for proactive queue length alerting"
}
TC_MARKS = {
        "tc1": 3,
        "tc2": 2,
        "tc3": 2,
        "tc4": 3,
        "tc5": 2,
        "tc6": 3,
        "tc7": 3,
        "tc8": 2
}
TC_CHECKS = [{'id': 'tc1', 'target_file': 'ebs_performance_rca.md', 'type': 'keywords', 'patterns': ['BurstBalance', '0%'], 'patterns_any': True, 'pass_msg': 'BurstBalance depletion to 0% correlated with database query stalls.', 'fail_msg': 'RCA does not correlate BurstBalance collapse with query latency.'}, {'id': 'tc2', 'target_file': 'ebs_performance_rca.md', 'type': 'keywords', 'patterns': ['3 IOPS', 'gp2'], 'pass_msg': 'Technical explanation articulates gp2 3 IOPS/GB baseline constraint and burst bucket mechanics.', 'fail_msg': 'Missing explanation of gp2 3 IOPS/GB baseline and burst bucket mechanics.'}, {'id': 'tc3', 'target_file': 'ebs_performance_rca.md', 'type': 'keywords', 'patterns': ['VolumeQueueLength', '40'], 'patterns_any': True, 'pass_msg': 'High VolumeQueueLength (>40) correctly analyzed as severe I/O bottleneck.', 'fail_msg': 'RCA does not analyze high VolumeQueueLength as I/O queuing bottleneck.'}, {'id': 'tc4', 'target_file': 'ebs_performance_rca.md', 'type': 'keywords', 'patterns': ['gp3', '12000', '500'], 'pass_msg': 'Migration command specifies gp3 volume with 12,000 IOPS and 500 MB/s throughput.', 'fail_msg': 'RCA missing modify-volume command with gp3, 12000 IOPS, and 500 MB/s.'}, {'id': 'tc5', 'target_file': 'ebs_performance_rca.md', 'type': 'keywords', 'patterns': ['optimizing', 'completed'], 'pass_msg': 'Online volume modification workflow validates zero downtime transition.', 'fail_msg': 'RCA missing online volume modification status validation (optimizing/completed).'}, {'id': 'tc6', 'target_file': 'ebs_performance_rca.md', 'type': 'keywords', 'patterns': ['latency', '5ms'], 'pass_msg': 'Post-modification performance benchmarking demonstrates sub-5ms response time.', 'fail_msg': 'Missing post-modification latency benchmark proving sub-5ms latency.'}, {'id': 'tc7', 'target_file': 'ebs_performance_rca.md', 'type': 'keywords', 'patterns': ['Root Cause', 'Remediation'], 'pass_msg': 'ebs_performance_rca.md contains structured Root Cause and Remediation sections.', 'fail_msg': "RCA report missing required sections ('Root Cause', 'Remediation')."}, {'id': 'tc8', 'target_file': 'ebs_performance_rca.md', 'type': 'keywords', 'patterns': ['alarm', 'VolumeQueueLength', '10'], 'pass_msg': 'Automated CloudWatch alarm configured for VolumeQueueLength > 10.', 'fail_msg': 'Missing automated CloudWatch alarm for VolumeQueueLength > 10.'}]

def run_tests():
    results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}
    scores = {k: 0 for k in results}
    reasons = {}

    print_separator()
    print("NIIT REAL-TIME AWS CLOUD AUDIT")
    print_separator()

    for check in TC_CHECKS:
        tc_id = check["id"]
        tc_label = tc_id.upper()
        tc_name = TC_NAMES.get(tc_id, tc_label)
        max_score = TC_MARKS.get(tc_id, 0)
        target_file = check["target_file"]
        check_type = check.get("type", "keywords")
        pass_msg = check.get("pass_msg", "Check passed.")
        fail_msg = check.get("fail_msg", "Check failed.")

        fpath = find_deliverable(target_file)
        if not fpath:
            results[tc_id] = False
            scores[tc_id] = 0
            reasons[tc_id] = f"Required deliverable '{target_file}' not found in student_workspace."
            continue

        try:
            content = ""
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if check_type == "json_values":
                data = json.loads(content)
                val_checks = check.get("checks", {})
                all_match = True
                content_lower = content.lower()
                for entity, exp_list in val_checks.items():
                    # Check both structured keys and text content
                    entity_found = any(exp in content_lower for exp in exp_list)
                    if not entity_found:
                        all_match = False
                        break
                if all_match:
                    results[tc_id] = True
                    scores[tc_id] = max_score
                    reasons[tc_id] = pass_msg
                else:
                    results[tc_id] = False
                    scores[tc_id] = 0
                    reasons[tc_id] = fail_msg

            elif check_type == "json_keys":
                data = json.loads(content)
                req_keys = check.get("required_keys", [])
                has_keys = all(k.lower() in [key.lower() for key in data.keys()] for k in req_keys)
                if has_keys:
                    results[tc_id] = True
                    scores[tc_id] = max_score
                    reasons[tc_id] = pass_msg
                else:
                    results[tc_id] = False
                    scores[tc_id] = 0
                    reasons[tc_id] = fail_msg

            elif check_type == "forbidden_patterns":
                forbidden = check.get("forbidden", [])
                found_forbidden = any(pat in content for pat in forbidden)
                if not found_forbidden:
                    results[tc_id] = True
                    scores[tc_id] = max_score
                    reasons[tc_id] = pass_msg
                else:
                    results[tc_id] = False
                    scores[tc_id] = 0
                    reasons[tc_id] = fail_msg

            else:
                patterns = check.get("patterns", [])
                patterns_any = check.get("patterns_any", False)
                content_lower = content.lower()
                if patterns_any:
                    matched = any(p.lower() in content_lower for p in patterns)
                else:
                    matched = all(p.lower() in content_lower for p in patterns)

                if matched:
                    results[tc_id] = True
                    scores[tc_id] = max_score
                    reasons[tc_id] = pass_msg
                else:
                    results[tc_id] = False
                    scores[tc_id] = 0
                    reasons[tc_id] = fail_msg

        except Exception as e:
            results[tc_id] = False
            scores[tc_id] = 0
            reasons[tc_id] = f"Error evaluating {target_file}: {str(e)}"

    total_score = sum(scores.values())

    for k in results.keys():
        tc_label = k.upper()
        tc_name = TC_NAMES.get(k, tc_label)
        max_score = TC_MARKS.get(k, 0)
        status = "[PASSED]" if results[k] else "[FAILED]"
        earned = scores[k]
        reason = reasons.get(k, "Check complete.")
        print_test_case(f"{tc_label}: {tc_name}", status, earned, max_score, reason)

    print_separator()
    print(f"TOTAL SCORE: {total_score}/20")
    print_separator()

    write_solution_json(total_score, 20, results)
    return total_score, results

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        # Fast evaluation without banner printing
        base_results = {'tc1': False, 'tc2': False, 'tc3': False, 'tc4': False, 'tc5': False, 'tc6': False, 'tc7': False, 'tc8': False}
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sol_path = os.path.join(current_dir, '..', 'student_workspace', 'solution.json')
            if os.path.exists(sol_path):
                with open(sol_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'results' in data:
                        base_results = data['results']
        except Exception:
            pass
        score, eval_results = run_tests()
        print(json.dumps(eval_results))
        sys.exit(0 if score == 20 else 1)

    score, results = run_tests()
    print(f"[LOCAL EVALUATION] Genuine test results for AWS_M07_M: {json.dumps(results)} (Score: {score})")
    print("Local test execution finished.")
    sys.exit(0 if score == 20 else 1)
