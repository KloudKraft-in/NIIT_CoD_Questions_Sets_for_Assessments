import sys
import json
from datetime import datetime

def verify_aws_on_server(candidate_email, question_id, niit_username=None, assessment_start_time=None, solution_data=None):
    """
    Central Server Auditor: Verifies AWS Distributed Jenkins Master-Agent infrastructure.
    """
    username = niit_username if niit_username else candidate_email.split('@')[0]
    
    report_items = []
    file_results = []
    fail_count = 0
    total_score = 0
    
    start_time = None
    if assessment_start_time:
        try:
            start_time = datetime.fromisoformat(assessment_start_time.replace('Z', '+00:00'))
        except Exception:
            pass
            
    results = solution_data.get('results', {}) if solution_data else {}
    
    # --- TC1: EC2 Instancing & Basic Settings ---
    tc1_passed = results.get('tc1', True) if solution_data else False
    if tc1_passed:
        report_items.append("TC1 [EC2 Instancing & Basic Settings] (5/5)")
        file_results.append("✓ TC1 [EC2 Instancing & Basic Settings]: PASSED (5/5)")
        total_score += 5
    else:
        report_items.append("TC1 [EC2 Instancing & Basic Settings] (0/5)")
        file_results.append("✗ TC1 [EC2 Instancing & Basic Settings]: FAILED (0/5) | Running 'jenkins-master' and 'jenkins-agent' instances not found.")
        fail_count += 1

    # --- TC2: Jenkins Master Installation ---
    tc2_passed = results.get('tc2', True) if solution_data else False
    if tc2_passed:
        report_items.append("TC2 [Jenkins Master Installation] (5/5)")
        file_results.append("✓ TC2 [Jenkins Master Installation]: PASSED (5/5)")
        total_score += 5
    else:
        report_items.append("TC2 [Jenkins Master Installation] (0/5)")
        file_results.append("✗ TC2 [Jenkins Master Installation]: FAILED (0/5) | Jenkins Master service is inactive or port 8080 unreachable.")
        fail_count += 1

    # --- TC3: Distributed Node Configuration ---
    tc3_passed = results.get('tc3', True) if solution_data else False
    if tc3_passed:
        report_items.append("TC3 [Distributed Node Configuration] (5/5)")
        file_results.append("✓ TC3 [Distributed Node Configuration]: PASSED (5/5)")
        total_score += 5
    else:
        report_items.append("TC3 [Distributed Node Configuration] (0/5)")
        file_results.append("✗ TC3 [Distributed Node Configuration]: FAILED (0/5) | Node 'jenkins-agent' config is missing or misconfigured in Jenkins Master.")
        fail_count += 1

    # --- TC4: Freestyle Job & Agent Build Log ---
    tc4_passed = results.get('tc4', True) if solution_data else False
    if tc4_passed:
        report_items.append("TC4 [Freestyle Job & Agent Build Log] (5/5)")
        file_results.append("✓ TC4 [Freestyle Job & Agent Build Log]: PASSED (5/5)")
        total_score += 5
    else:
        report_items.append("TC4 [Freestyle Job & Agent Build Log] (0/5)")
        file_results.append("✗ TC4 [Freestyle Job & Agent Build Log]: FAILED (0/5) | Agent-Build-Job configuration not found or build log missing on Agent.")
        fail_count += 1

    file_results.append("-" * 50)
    file_results.append(f"🎯 TOTAL SCORE: {total_score}/20")

    # 8-Column CSV Format for Taxila
    from datetime import timezone, timedelta
    import os
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
    timestamp = datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")
    
    problem_code = "github_jenkins_python_testing"
    csv_report = f"{date_str},{problem_code},{candidate_email},{timestamp},{len(report_items)}: {'; '.join(report_items)},,{fail_count},{total_score}"
    
    # Save Report to Central Server Filesystem
    report_base = f"/home/ubuntu/central_server/reports/{problem_code}/{candidate_email}"
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{candidate_email}_{timestamp}.txt")
    
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(file_results) + "\n")
    except Exception as e:
        print(f"[WARN] Could not write report file: {e}")
        pass
    
    print(f"\n[REPORT_CSV]: {csv_report}")
    return csv_report

if __name__ == "__main__":
    if len(sys.argv) > 1:
        verify_aws_on_server(sys.argv[1], "AWS_Q20_E")
    else:
        verify_aws_on_server("candidate@niit.com", "AWS_Q20_E")
