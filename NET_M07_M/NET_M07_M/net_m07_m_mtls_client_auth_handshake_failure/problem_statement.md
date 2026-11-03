# Network Troubleshooting: Mutual TLS (mTLS) Client Authentication Handshake Triage

Duration : 60 Min.

## Scenario

An enterprise payments backend transitions to a Zero Trust architecture requiring Mutual TLS (mTLS) for all partner integrations. Partner payment gateways calling `https://mtls-pay.enterprise.com:8443` report that their API clients receive `SSL alert number 48: unknown CA` and connections immediately abort during the TLS handshake. Standard one-way HTTPS testing succeeds, but client-authenticated calls fail. The network security engineer captured detailed `openssl s_client` debug traces with client certificates, the server CA truststore inventory, and server NGINX SSL configuration. The engineer must diagnose why the server rejects the partner client certificate.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `ca_truststore_list.pem`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `nginx_mtls.conf`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `openssl_mtls_client_trace.log`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `client_cert_chain.pem`, `nginx_mtls_ssl_error.log`, and `ca_truststore_bundle.pem` in `student_workspace/`.
3. Trace the bidirectional certificate exchange and verification phases of the mTLS handshake.
4. Inspect certificate validity, key usage, Extended Key Usage (EKU) extensions, and issuer authorities for both client and server certificates.
5. Analyze the server error logs to pinpoint the exact failure reason during client certificate verification.
6. Specify the corrective certificate issuance parameters and server truststore configuration in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Detailed evaluation of mutual TLS handshake mechanics and bidirectional certificate validation | 3 Marks |
| **Rubric 2** | Thorough inspection of x509 certificate attributes, Key Usage, and EKU extensions | 3 Marks |
| **Rubric 3** | Accurate diagnosis of the root cause in the trust store or certificate chain | 2 Marks |
| **Rubric 4** | Technical distinction between server certificate verification and client certificate verification | 2 Marks |
| **Rubric 5** | Formulation of the corrected CA truststore bundle and server configuration directives | 2 Marks |
| **Rubric 6** | Specification of compliant client certificate generation and signing parameters | 2 Marks |
| **Rubric 7** | Design of automated certificate validation preflight testing procedures | 3 Marks |
| **Rubric 8** | Comprehensive incident report detailing root cause, remediation, and security implications | 3 Marks |

**Total Score: 20 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
