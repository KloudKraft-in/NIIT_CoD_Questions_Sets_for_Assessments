# Network Troubleshooting: Enterprise Edge NAT Port Exhaustion & Connection Dropping

Duration : 60 Min.

## Scenario

During a massive enterprise-wide software update roll-out to 25,000 corporate laptops, internet connectivity abruptly collapses across all corporate office locations. Users cannot browse web pages or connect to SaaS services. Internal LAN connectivity remains unaffected. An engineer captured firewall connection tracking statistics, edge drop syslog entries, and client port allocation metrics. The network security engineer must analyze these artifacts, diagnose the root cause of the edge connectivity collapse, and specify both immediate mitigations and architectural upgrades.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `client_port_allocation.csv`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `edge_drop_syslog.log`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `firewall_connection_table_stats.json`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `nat_gateway_metrics.csv`, `firewall_conntrack_table.txt`, and `dns_drop_events.log` in `student_workspace/`.
3. Analyze NAT gateway metric trends, connection tracking table state, and outbound packet drop counters.
4. Examine the connection tracking table to identify top talkers, connection states, and protocol distributions.
5. Determine the exact network failure mechanism causing high packet drop rates during peak traffic.
6. Formulate short-term operational mitigations and long-term network architecture upgrades to eliminate NAT bottlenecks in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Quantitative analysis of NAT gateway metrics and connection tracking table capacity | 3 Marks |
| **Rubric 2** | Identification of traffic patterns and top talkers contributing to connection table saturation | 3 Marks |
| **Rubric 3** | Technical explanation of source port exhaustion and conntrack table behavior | 2 Marks |
| **Rubric 4** | Correlation of NAT table drops with application-level DNS and HTTP failures | 2 Marks |
| **Rubric 5** | Formulation of immediate operational tuning (TCP timeout reductions and table resizing) | 2 Marks |
| **Rubric 6** | Design of architectural capacity enhancements (additional egress IPs / pool expansion) | 2 Marks |
| **Rubric 7** | Evaluation of application connection pooling to minimize ephemeral port usage | 3 Marks |
| **Rubric 8** | Creation of an alerting and monitoring baseline for early detection of NAT exhaustion | 3 Marks |

**Total Score: 20 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
