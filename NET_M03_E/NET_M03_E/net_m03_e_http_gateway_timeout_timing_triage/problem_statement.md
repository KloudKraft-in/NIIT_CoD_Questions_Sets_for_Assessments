# Network Troubleshooting: HTTP 504 Gateway Timeout Latency Breakdown

Duration : 45 Min.

## Scenario

A payments processing API gateway throws intermittent `HTTP 504 Gateway Timeout` errors during end-of-month reconciliation runs. The developers blame the network team, claiming network packet loss between the API gateway and backend worker servers. An engineer captured detailed request timing metrics using `curl -w` and upstream gateway access logs. The network engineer must inspect these timing metrics, isolate the exact phase where latency accumulates, and differentiate between network transport failure and upstream processing delays.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `curl_timing_breakdown.log`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `gateway_upstream_access.log`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `curl_latency_waterfall.log` and `upstream_app_timings.csv` in `student_workspace/`.
3. Break down the end-to-end request latency across DNS resolution, TCP handshake, TLS negotiation, Time to First Byte (TTFB), and data transfer.
4. Correlate edge proxy timeout settings with upstream microservice processing times.
5. Determine whether the HTTP 504 Gateway Timeout stems from network transmission latency, edge proxy configuration, or backend processing delays.
6. Formulate an infrastructure and proxy tuning plan to resolve timeouts in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Detailed mathematical breakdown of HTTP request phases from curl telemetry | 3 Marks |
| **Rubric 2** | Accurate isolation of latency bottlenecks across network, proxy, and application tiers | 3 Marks |
| **Rubric 3** | Technical explanation of 504 Gateway Timeout generation mechanics and threshold boundaries | 2 Marks |
| **Rubric 4** | Formulation of tuned proxy timeouts and upstream capacity recommendations | 2 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
