# Network Troubleshooting: Incomplete TLS Certificate Chain & Trust Verification

Duration : 30 Min.

## Scenario

A mobile banking app fails to connect to its backend API gateway `https://api.mobilepay.net`, logging `SEC_ERROR_UNKNOWN_ISSUER`, while desktop browsers access the endpoint without error. The systems engineer captured an `openssl s_client -showcerts` output. The engineer must inspect the certificate chain hierarchy, analyze the verification trace, explain why desktop browsers connect successfully while mobile devices fail, and specify the server-side certificate bundle fix.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `cert_chain_probe.log`: OpenSSL TLS certificate chain verification trace captured from the live service.
- `server_ssl_config.json`: Web server SSL/TLS certificate path and cipher suite configuration.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `cert_chain_probe.log` and `server_ssl_config.json` in `student_workspace/`.
3. Analyze the certificate depth hierarchy returned during the TLS handshake.
4. Explain the technical difference in how desktop browsers and mobile operating systems handle intermediate certificate discovery.
5. Identify the root cause behind the certificate validation error reported in the probe log.
6. Provide the corrective server configuration and certificate bundling procedure in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Accurate analysis of TLS certificate hierarchy and intermediate CA propagation | 4 Marks |
| **Rubric 2** | Clear technical explanation of client trust store validation differences | 3 Marks |
| **Rubric 3** | Specification of the correct certificate bundle construction and server configuration | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
