# Network Troubleshooting: Enterprise Multi-Branch Connectivity & Health Audit

Duration : 45 Min.

## Scenario

As a Network Operations Center (NOC) Tier 2 engineer, you receive automated alerts that 3 of 12 enterprise branch offices are experiencing intermittent portal outages. You are provided with a centralized telemetry log capturing ping latency/loss across all branches, a DNS resolution status matrix, and curl HTTP status checks. You must analyze these artifacts, determine the fault domain for each failing branch (local gateway drop vs. DNS failure vs. application HTTP 500), and produce the enterprise connectivity scorecard.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `dns_resolution_matrix.json`: DNS query resolution results for internal domains across corporate branches.  
- `http_endpoint_audit.log`: HTTP endpoint response audit log capturing status codes across all branch sites.  
- `multi_branch_ping.csv`: Matrix of ICMP ping reachability across 12 enterprise branch offices.  
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Inspect `multi_branch_ping.csv`, `dns_resolution_matrix.json`, and `http_endpoint_audit.log` in `student_workspace/`.
3. Analyze the connectivity, name resolution, and HTTP response data across all 12 corporate branch offices.
4. For every branch exhibiting failure or degraded performance, isolate the specific network or application layer where the breakdown occurs.
5. Compile an enterprise branch connectivity scorecard detailing operational status, fault domain, and root cause evidence.
6. Provide prioritized operational remediation recommendations for the enterprise network operations team in `student_workspace/triage_report.md`.

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
| :---- | :---- | :---- |
| **Rubric 1** | Comprehensive multi-tier audit evaluating all branch offices across network, DNS, and application layers | 4 Marks |
| **Rubric 2** | Accurate fault-domain isolation and root cause determination for every failing branch | 3 Marks |
| **Rubric 3** | Clear, structured operational scorecard and prioritized remediation plan | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.  
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.  
- &nbsp;