# Network Troubleshooting: Port & Certificate Preflight Testing

Duration : 30 Min.

## Scenario

Before deploying a new automated logistics integration, a systems administrator executed pre-flight port and certificate tests against endpoint `logistics-edi.freight.com` on port 8443. The administrator ran both `nc -zv` (raw Layer 4 TCP check) and `openssl s_client` (Layer 7 TLS handshake check). The engineer must analyze the captured output logs to explain why a successful TCP port connection does not guarantee application communication if TLS handshake negotiation fails.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `legacy_client_handshake_failure.log`: Client application TLS negotiation error and handshake failure trace.
- `nc_port_probe.log`: TCP port reachability scan results for the target database gateway.
- `openssl_s_client.txt`: Captured OpenSSL s_client handshake output and certificate chain telemetry.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Inspect `nc_port_probe.log`, `openssl_s_client.txt`, and `legacy_client_handshake_failure.log` in `student_workspace/`.
3. Analyze the Layer 4 port probe output and explain what it verifies regarding transport-layer reachability.
4. Inspect the cryptographic handshake output, evaluating the negotiated TLS protocol version, cipher suite, and certificate status.
5. Correlate the client failure logs with the gateway capabilities to determine the root cause of the connection failure.
6. Document your technical findings and client/server remediation plan in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Accurate interpretation of Layer 4 transport connectivity and port testing outputs | 4 Marks |
| **Rubric 2** | Thorough evaluation of TLS negotiation parameters, protocol versions, and certificates | 3 Marks |
| **Rubric 3** | Identification of the root cause of the client failure with actionable remediation | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
