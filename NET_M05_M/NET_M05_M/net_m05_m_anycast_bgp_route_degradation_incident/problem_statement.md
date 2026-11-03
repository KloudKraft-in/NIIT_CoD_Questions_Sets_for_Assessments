# Network Troubleshooting: Anycast BGP Route Degradation & Latency Variance Incident

Duration : 60 Min.

## Scenario

A global edge Anycast DNS service (198.51.100.53) experiences severe performance degradation. European clients in London, Paris, and Frankfurt experience latency climbing from 10 ms to 320 ms. Synthetic monitoring detects that European traffic is not being routed to the Frankfurt Anycast edge node, but is crossing the trans-Pacific cable to the Tokyo edge node. The network operations team captured BGP Looking Glass route tables from global transit providers, global ping telemetry, and traceroute captures. The network engineer must inspect these artifacts, determine why traffic is diverted away from the local edge node, isolate the routing anomaly, and formulate the BGP routing policy fix.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `bgp_looking_glass_routes.txt`: Public BGP looking glass route server output for company Anycast prefixes.
- `global_ping_latency_matrix.csv`: Global probe latency and packet loss matrix for Anycast edge locations.
- `traceroute_anycast_fleet.log`: Traceroute telemetry from distributed global monitoring probes to Anycast VIP.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `bgp_looking_glass_routes.txt`, `traceroute_anycast_fleet.log`, and `global_ping_latency_matrix.csv` in `student_workspace/`.
3. Analyze BGP route advertisements, Autonomous System (AS) paths, and prefix announcements across global looking glass nodes.
4. Correlate global latency spikes and traceroute hops to identify path sub-optimality or route poisoning.
5. Determine the primary routing anomaly causing sub-optimal traffic steering and high latency for regional users.
6. Formulate BGP traffic engineering strategies (AS-path prepending, community tags, or route filters) to restore optimal global routing in `student_workspace/triage_report.md`.

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
| **Rubric 1** | In-depth analysis of BGP route paths, AS sequences, and prefix propagation | 3 Marks |
| **Rubric 2** | Correlation of global looking glass telemetry with regional latency degradation | 3 Marks |
| **Rubric 3** | Identification of the routing anomaly causing traffic diversion | 2 Marks |
| **Rubric 4** | Evaluation of Anycast routing behavior and edge node selection | 2 Marks |
| **Rubric 5** | Formulation of BGP traffic engineering remediation (AS-path prepending / community tagging) | 2 Marks |
| **Rubric 6** | Design of route monitoring and health-check automation to prevent recurrence | 2 Marks |
| **Rubric 7** | Assessment of transit provider SLA compliance and packet loss metrics | 3 Marks |
| **Rubric 8** | Comprehensive production post-incident review and operational documentation | 3 Marks |

**Total Score: 20 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
