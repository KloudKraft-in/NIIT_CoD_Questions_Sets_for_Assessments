# Network Troubleshooting: Path MTU Discovery & WAN Blackhole Triage

Duration : 45 Min.

## Scenario

A financial analytics application connecting branch offices to a cloud database cluster reports that small SQL queries execute in under 20 ms, while large reporting queries with result sets exceeding 1,500 bytes hang indefinitely and time out. An engineer gathered bidirectional traceroute outputs and MTU ping probes with the Don't Fragment (DF) bit set. The engineer must inspect these artifacts, identify the path MTU bottleneck and asymmetric route latency, and specify the TCP MSS clamping fix.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `pmtu_ping_sweep.log`: Path MTU ICMP sweep test log across WAN connections.
- `sql_client_trace.log`: Database client communication trace capturing transaction timeouts and query hangs.
- `traceroute_outbound.log`: Outbound WAN traceroute capture across transit and IPsec tunnel hops.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `traceroute_outbound.log`, `pmtu_ping_sweep.log`, and `sql_client_trace.log` in `student_workspace/`.
3. Analyze the WAN network path and identify hops exhibiting MTU constraints or ICMP response anomalies.
4. Correlate the database client trace with the packet sweep results to diagnose why large data queries stall while basic connectivity succeeds.
5. Calculate the effective Maximum Segment Size (MSS) required to prevent fragmentation blackholing across the path.
6. Formulate network and edge configuration changes to permanently eliminate query freezes in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Precise path analysis locating MTU bottleneck hops and ICMP filtering behavior | 4 Marks |
| **Rubric 2** | Accurate mathematical calculation of protocol overhead and optimal TCP MSS values | 3 Marks |
| **Rubric 3** | Formulation of robust network and edge transport configurations to resolve the stall | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
