# Network Troubleshooting: Multi-Host TLS Fleet Expiry & SAN Compliance Audit

Duration : 45 Min.

## Scenario

Following an unexpected outage caused by an expired certificate on an internal auth proxy, the network security team is tasked with auditing the SSL/TLS certificate fleet across 10 critical public-facing and internal services. An automated crawler collected certificate metadata including issuer, validity dates, days to expiry, key algorithms, and Subject Alternative Names (SAN). The engineer must inspect the fleet audit report, flag high-risk certificates, detect SAN omissions, and establish an automated renewal schedule.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `fleet_ssl_audit.json`: Corporate domain SSL certificate inventory and expiration audit data.
- `pki_governance_policy.txt`: Enterprise PKI governance and certificate renewal security policy.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `fleet_ssl_audit.json` and `pki_governance_policy.txt` in `student_workspace/`.
3. Audit the entire fleet of domain endpoints against enterprise cryptographic and certificate lifecycle policies.
4. Classify all endpoints into risk tiers based on expiration timelines, Subject Alternative Name (SAN) coverage, and cipher strength.
5. Identify all non-compliant endpoints and analyze the exact technical failure condition each would cause for client applications.
6. Construct a prioritized PKI remediation and certificate lifecycle renewal roadmap in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Systematic fleet audit accurately classifying endpoints across expiry and policy compliance tiers | 4 Marks |
| **Rubric 2** | Rigorous technical analysis of SAN coverage, host matching, and client handshake impacts | 3 Marks |
| **Rubric 3** | Formulation of a prioritized, risk-weighted certificate renewal and governance roadmap | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
