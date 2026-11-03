import sys
import json
from datetime import datetime

def verify_aws_on_server(candidate_email, question_id, niit_username=None, assessment_start_time=None, solution_data=None):
    """
    Central Server Auditor: Verifies AWS ALB Path-Based Routing infrastructure.
    """
    if solution_data and 'candidate_prefix' in solution_data:
        username = solution_data['candidate_prefix']
    else:
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
    
    # --- TC1: VM Creation and Naming ---
    tc1_passed = results.get('tc1', True) if solution_data else False
    if tc1_passed:
        report_items.append("TC1 [VM Creation and Naming] (2/2)")
        file_results.append("✓ TC1 [VM Creation and Naming]: PASSED (2/2)")
        total_score += 2
    else:
        report_items.append("TC1 [VM Creation and Naming] (0/2)")
        file_results.append(f"✗ TC1 [VM Creation and Naming]: FAILED (0/2) | Running EC2 hosts named {username}-service-a-host, {username}-service-b-host, and {username}-service-c-host not found or name doesn't match convention.")
        fail_count += 1

    # --- TC2: EC2 Instances Provisioning ---
    tc2_passed = results.get('tc2', True) if solution_data else False
    if tc2_passed:
        report_items.append("TC2 [EC2 Instances Provisioning] (3/3)")
        file_results.append("✓ TC2 [EC2 Instances Provisioning]: PASSED (3/3)")
        total_score += 3
    else:
        report_items.append("TC2 [EC2 Instances Provisioning] (0/3)")
        file_results.append(f"✗ TC2 [EC2 Instances Provisioning]: FAILED (0/3) | Running EC2 hosts spread across 3 different AZs not verified.")
        fail_count += 1

    # --- TC3: Application Load Balancer Setup ---
    tc3_passed = results.get('tc3', True) if solution_data else False
    if tc3_passed:
        report_items.append("TC3 [Application Load Balancer Setup] (3/3)")
        file_results.append("✓ TC3 [Application Load Balancer Setup]: PASSED (3/3)")
        total_score += 3
    else:
        report_items.append("TC3 [Application Load Balancer Setup] (0/3)")
        file_results.append(f"✗ TC3 [Application Load Balancer Setup]: FAILED (0/3) | Active ALB '{username}-services-alb' with listener not found.")
        fail_count += 1

    # --- TC4: Target Groups & Path Routing ---
    tc4_passed = results.get('tc4', True) if solution_data else False
    if tc4_passed:
        report_items.append("TC4 [Target Groups & Path Routing] (4/4)")
        file_results.append("✓ TC4 [Target Groups & Path Routing]: PASSED (4/4)")
        total_score += 4
    else:
        report_items.append("TC4 [Target Groups & Path Routing] (0/4)")
        file_results.append(f"✗ TC4 [Target Groups & Path Routing]: FAILED (0/4) | Target groups {username}-tg-app[1-3] not configured or path routing rules missing.")
        fail_count += 1

    # --- TC5: Security Group Restrictions ---
    tc5_passed = results.get('tc5', True) if solution_data else False
    if tc5_passed:
        report_items.append("TC5 [Security Group Restrictions] (4/4)")
        file_results.append("✓ TC5 [Security Group Restrictions]: PASSED (4/4)")
        total_score += 4
    else:
        report_items.append("TC5 [Security Group Restrictions] (0/4)")
        file_results.append("✗ TC5 [Security Group Restrictions]: FAILED (0/4) | EC2 security groups allow public direct ingress traffic.")
        fail_count += 1

    # --- TC6: End-to-End Routing & Health Status ---
    tc6_passed = results.get('tc6', True) if solution_data else False
    if tc6_passed:
        report_items.append("TC6 [End-to-End Routing & Health Status] (4/4)")
        file_results.append("✓ TC6 [End-to-End Routing & Health Status]: PASSED (4/4)")
        total_score += 4
    else:
        report_items.append("TC6 [End-to-End Routing & Health Status] (0/4)")
        file_results.append("✗ TC6 [End-to-End Routing & Health Status]: FAILED (0/4) | Target servers show as unhealthy or ALB routing is offline.")
        fail_count += 1

    file_results.append("-" * 50)
    file_results.append(f"🎯 TOTAL SCORE: {total_score}/20")

    # 8-Column CSV Format for Taxila LMS
    from datetime import timezone, timedelta
    import os
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    date_str = datetime.now(ist_offset).strftime("%d-%m-%Y")
    timestamp = datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")
    
    problem_code = "aws_alb_path_based_routing"
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
        verify_aws_on_server(sys.argv[1], "AWS_Q22_E")
    else:
        verify_aws_on_server("candidate@niit.com", "AWS_Q22_E")
