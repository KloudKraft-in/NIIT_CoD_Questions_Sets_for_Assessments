# Network Troubleshooting: Path Diagnostics & Hop-by-Hop Traceroute Analysis

Duration : 30 Min.

## Scenario

A payments microservice reports intermittent 2,000 ms latency spikes when calling an external banking partner API. An operations engineer executed a traceroute trace against the partner endpoint (`api.partnerbank.com`) and captured the output. The engineer must interpret this traceroute log, distinguish between intentional ICMP rate limiting and a genuine routing bottleneck, and determine whether the issue is internal or upstream in the carrier transit network.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `route_hop_registry.csv`: Autonomous System (AS) and network ownership registry for transit hops along the path.
- `traceroute_partnerbank.log`: Hop-by-hop traceroute execution log capturing round-trip times to partner bank gateway.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `traceroute_partnerbank.log` and `route_hop_registry.csv` in `student_workspace/`.
3. Analyze the hop-by-hop latency and probe responses across the entire network path.
4. Evaluate any hops displaying non-responses (`* * *`) and provide technical justification for whether they indicate network failure or router control-plane behavior.
5. Identify the specific network segment where latency degradation originates based on the telemetry data.
6. Correlate hop ownership to formulate a targeted vendor or carrier escalation ticket in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Accurate technical interpretation of intermediate router responses and hop behavior | 4 Marks |
| **Rubric 2** | Precise identification of the bottleneck segment where latency degradation originates | 3 Marks |
| **Rubric 3** | Correct attribution of ownership and formulation of an actionable escalation ticket | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
