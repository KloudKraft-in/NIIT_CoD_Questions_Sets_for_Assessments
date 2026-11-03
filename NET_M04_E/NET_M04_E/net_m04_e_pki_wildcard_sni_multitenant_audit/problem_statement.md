# Network Troubleshooting: PKI Wildcard & Server Name Indication (SNI) Routing Audit

Duration : 45 Min.

## Scenario

A SaaS provider hosts multiple customer virtual hosts on a shared public IP address using NGINX. Customer users accessing `https://tenant1.app.enterprise.com` report receiving an SSL warning that the site certificate belongs to `default-fallback.enterprise.com`. Meanwhile, users accessing `https://app.enterprise.com` experience no warnings. An engineer captured `openssl s_client` results with and without the `-servername` (SNI) flag and the web server virtual host configuration. The engineer must diagnose why specific subdomains fail certificate validation and determine the required server and certificate configuration.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `multi_vhost_ssl_scan.txt`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `virtual_hosts.conf`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `sni_client_hello_dump.txt`, `edge_vhost_ssl.conf`, and `pki_cert_inventory.json` in `student_workspace/`.
3. Analyze the TLS Client Hello payload and verify the Server Name Indication (SNI) extension.
4. Evaluate the virtual host SSL configurations on the edge server to trace which certificate is selected during the handshake.
5. Determine why client requests for specific subdomains fail certificate validation while other domains on the same IP succeed.
6. Formulate the required edge server virtual host and certificate configuration directives in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Rigorous inspection of TLS Client Hello extensions and SNI negotiation parameters | 3 Marks |
| **Rubric 2** | Accurate diagnosis of virtual host certificate mapping and wildcard domain matching rules | 3 Marks |
| **Rubric 3** | Technical explanation of multi-tenant TLS hosting on shared IP infrastructure | 2 Marks |
| **Rubric 4** | Formulation of the corrected virtual host configuration to ensure proper certificate delivery | 2 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
