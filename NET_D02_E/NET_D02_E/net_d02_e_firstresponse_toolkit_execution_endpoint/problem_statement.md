# Network Troubleshooting: First-Response Toolkit Execution & Endpoint Triage

Duration : 30 Min.

## Scenario

Before certifying a newly provisioned branch office for go-live, an engineer executed the standard first-response connectivity check suite against five critical enterprise endpoints: (1) Primary Domain Controller (10.10.1.10), (2) External Corporate Portal (portal.acme.corp), (3) Cloud Payment Gateway (api.paygateway.com), (4) Internal HR Intranet (hr.local), and (5) Public DNS (8.8.8.8). The engineer must analyze the captured command logs, identify which targets failed, and explain why jumping directly to curl without validating DNS is a diagnostic anti-pattern.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `branch_ping_test.log`: Captured ICMP ping probe output across regional branch network endpoints.
- `curl_test_report.log`: HTTP/HTTPS connection probe results and status codes for audited endpoints.
- `nslookup_output.txt`: DNS lookup output for corporate internal and external target domains.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Inspect `branch_ping_test.log`, `nslookup_output.txt`, and `curl_test_report.log` in `student_workspace/`.
3. Evaluate the diagnostic results for all target endpoints across interface, DNS, ICMP, and HTTP layers.
4. For each failing or anomalous endpoint, analyze the root cause behind the observed output and differentiate transport/network filtering from genuine service unavailability.
5. Explain the operational importance of following a structured diagnostic sequence rather than jumping directly to application-layer tests.
6. Complete an endpoint verification matrix and documented findings in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Comprehensive diagnostic analysis and accurate health determination across all target endpoints | 4 Marks |
| **Rubric 2** | Accurate technical interpretation distinguishing between protocol filtering and service failure | 3 Marks |
| **Rubric 3** | Methodical ordering of first-response diagnostics with operational justification | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
