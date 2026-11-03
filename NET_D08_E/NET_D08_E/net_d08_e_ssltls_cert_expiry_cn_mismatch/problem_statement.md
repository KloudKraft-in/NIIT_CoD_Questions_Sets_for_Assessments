# Network Troubleshooting: SSL/TLS Certificate Expiry & Name Validation Triage

Duration : 30 Min.

## Scenario

Customers accessing a banking portal `https://secure.pay.acmebank.com` report receiving a browser security warning: 'Your connection is not private (NET::ERR_CERT_COMMON_NAME_INVALID)'. The server administrator claims the certificate was just renewed yesterday and is valid for 1 year. The network security engineer captured the certificate text dump using `openssl x509 -text -noout` and the browser security warning log. The engineer must inspect these artifacts, identify the exact reason for the security warning, and specify the remediation.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `browser_security_alert.log`: Client browser security warning logs and TLS validation error codes.
- `openssl_cert_dump.txt`: Decoded X.509 certificate dump containing validity dates and subject alternative names.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `openssl_cert_dump.txt` and `browser_security_alert.log` in `student_workspace/`.
3. Audit the certificate validity dates, issuer information, and Subject parameters from the x509 dump.
4. Inspect the Subject Common Name (CN) and Subject Alternative Name (SAN) extensions against the requested hostname.
5. Determine the exact technical condition triggering the client security alert.
6. Specify the remediation requirements and necessary certificate attributes for renewal/re-issuance in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Comprehensive verification of certificate validity periods and cryptographic metadata | 4 Marks |
| **Rubric 2** | Accurate analysis of hostname validation rules across Common Name and SAN extensions | 3 Marks |
| **Rubric 3** | Formulation of exact certificate specifications and remediation plan | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
