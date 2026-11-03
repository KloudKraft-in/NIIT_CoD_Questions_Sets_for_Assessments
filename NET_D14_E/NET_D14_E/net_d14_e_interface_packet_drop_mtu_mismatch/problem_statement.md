# Network Troubleshooting: Interface Packet Drops & Maximum Transmission Unit (MTU)

Duration : 30 Min.

## Scenario

A database replication pipeline over a VPN tunnel experiences recurring data stream freezes whenever bulk insert batches exceed 1,500 bytes, while small heartbeat queries pass with zero errors. An engineer captured interface statistics via `ip -s link show eth0` and a series of MTU ping sweep tests with the Don't Fragment (`DF`) bit set. The network engineer must inspect these artifacts, identify the MTU mismatch, and formulate the VPN interface clamp or MTU tuning fix.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `ip_link_stats.txt`: Network interface status, MTU settings, and packet drop counters.
- `ping_df_test.log`: ICMP ping sweep test log with Don't Fragment (DF) flag set at varying payload sizes.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `ip_link_stats.txt` and `ping_df_test.log` in `student_workspace/`.
3. Analyze the network interface configuration parameters and error counters across physical and virtual interfaces.
4. Evaluate the ping sweep results, calculate IP/ICMP protocol overhead, and determine the exact path MTU threshold where packet transmission fails.
5. Explain the phenomenon causing bulk TCP data transfers to hang while initial connections succeed.
6. Formulate network and transport layer remediation options to restore uninterrupted data synchronization in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Accurate calculation of protocol headers, framing overhead, and path MTU boundaries | 4 Marks |
| **Rubric 2** | Diagnosis of packet dropping behavior under DF-flagged fragmentation constraints | 3 Marks |
| **Rubric 3** | Formulation of viable transport/interface remediation strategies to resolve bulk transfer stalls | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
