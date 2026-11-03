# Network Troubleshooting: API Gateway Socket Pool Leak & File Descriptor Exhaustion

Duration : 60 Min.

## Scenario

A high-traffic e-commerce API gateway processing 10,000 requests/second begins throwing HTTP 502 Bad Gateway errors during flash sales. The application nodes report normal CPU (25%) and Memory (40%), but synthetic monitors indicate that new TCP connections are being refused. An SRE engineer gathered an `ss -tan` socket dump, kernel SNMP TCP statistics, and load balancer target health logs. The network engineer must analyze these artifacts, diagnose a massive `CLOSE_WAIT` socket descriptor leak combined with ephemeral port exhaustion, and define the complete code-level and OS kernel mitigation.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `alb_backend_pool_health.json`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `kernel_netstat_snmp.csv`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `ss_connection_dump.log`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `ss_tan_state_summary.txt`, `api_gateway_access.log`, and `thread_dump_summary.txt` in `student_workspace/`.
3. Perform a quantitative audit of the operating system socket table, process file descriptors, and connection states.
4. Correlate gateway upstream transaction logs with thread dump traces to isolate the socket lifecycle breakdown.
5. Determine the exact failure mechanism causing socket exhaustion and explain why new connections are refused.
6. Prescribe immediate operational recovery procedures and formulate code/architectural fixes to prevent recurrence in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Quantitative analysis of socket state distribution and OS file descriptor table utilization | 5 Marks |
| **Rubric 2** | Correlation of gateway access logs with thread execution states to identify the socket leak | 5 Marks |
| **Rubric 3** | Technical explanation of socket lifecycle mismanagement and OS resource limits | 5 Marks |
| **Rubric 4** | Formulation of immediate operational recovery steps and permanent architectural remediation | 5 Marks |

**Total Score: 20 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
