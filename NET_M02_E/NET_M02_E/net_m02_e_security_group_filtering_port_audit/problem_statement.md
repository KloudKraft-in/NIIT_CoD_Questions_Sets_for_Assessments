# Network Troubleshooting: Cloud Security Group & Network ACL Filtering Audit

Duration : 45 Min.

## Scenario

A newly provisioned web application tier (10.0.1.0/24) in an AWS VPC cannot reach backend PostgreSQL databases (10.0.2.0/24) on port 5432. The security team insists all security groups are configured correctly. An engineer captured Security Group rules, Subnet Network ACL rules, and `nc -zv` probe logs. The network engineer must inspect these artifacts, identify where and why the traffic is dropped in the firewall stack, and formulate the rule fix.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `port_scan_nc_results.log`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `security_group_rules.json`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `subnet_nacl_rules.csv`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `aws_security_group_rules.json`, `network_acl_rules.json`, and `nc_port_test_results.log` in `student_workspace/`.
3. Analyze inbound and outbound security group rules alongside subnet Network ACL rules for the target architecture.
4. Correlate port probe outputs with the filtering rules to determine which layer of the firewall stack dropped the traffic.
5. Explain the difference between stateful security groups and stateless Network ACLs in handling ephemeral return traffic.
6. Specify the exact rule adjustments required to permit authorized service communication in `student_workspace/triage_report.md`.

## Instructions to Perform the Task

1. Create the setup script `setup.sh` inside `student_workspace/`, grant execute permissions using `chmod +x setup.sh`, and run `./setup.sh`.
2. Review the scenario and inspect the pre-provisioned artifact files in your `student_workspace/`.
3. Formulate your technical diagnosis, packet/route analysis, and remediation plan based on the artifact evidence.
4. Save your comprehensive analysis inside `student_workspace/triage_report.md` (using `triage_report_template.md` as your guide).
5. Review your submission against the **Evaluation Rubric** below to ensure all technical criteria are addressed.
6. When complete, return to the platform dashboard and click **"Submit Final"**. This assessment is evaluated manually by the evaluation team.

## Validation

Once your deliverable is prepared and saved in the workspace, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:

| Item | Requirement / Criteria | Marks |
| :--- | :--- | :--- |
| **Rubric 1** | Comprehensive audit of cloud firewall rules across security group and NACL boundaries | 3 Marks |
| **Rubric 2** | Accurate isolation of the specific filtering rule or missing permission causing packet drops | 3 Marks |
| **Rubric 3** | Clear technical differentiation between stateful and stateless inspection rules | 2 Marks |
| **Rubric 4** | Formulation of a compliant, least-privilege security group and NACL update specification | 2 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
