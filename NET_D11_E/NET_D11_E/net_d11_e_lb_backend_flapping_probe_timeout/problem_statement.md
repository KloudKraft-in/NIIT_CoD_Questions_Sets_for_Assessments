# Network Troubleshooting: Load Balancer Backend Flapping & Timeout Tuning

Duration : 30 Min.

## Scenario

A payments cluster behind an internal load balancer experiences intermittent service disruptions. Monitoring alerts show that backend nodes repeatedly alternate between 'Healthy' and 'Unhealthy' every 60 seconds (flapping). The operations team captured ALB health transition event logs, application JVM garbage collection metrics, and probe settings. The network engineer must analyze these artifacts to identify why aggressive timeout settings cause false unhealthy flapping during routine garbage collection cycles.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `alb_event_history.log`: Application Load Balancer target state transition event timeline.
- `app_jvm_gc_metrics.csv`: Application JVM garbage collection pause telemetry and system metrics.
- `health_probe_settings.json`: Current load balancer health check probe configuration thresholds.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Inspect `alb_event_history.log`, `app_jvm_gc_metrics.csv`, and `health_probe_settings.json` in `student_workspace/`.
3. Analyze the timeline of backend state transitions and correlate them with application runtime performance metrics.
4. Explain the mechanism causing healthy backend instances to be repeatedly evicted from the active pool.
5. Formulate revised health probe parameters (timeout, interval, threshold) that maintain rapid failure detection while preventing false-positive evictions.
6. Document your technical analysis and revised probe baseline in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Correlation of load balancer state transition events with application runtime telemetry | 4 Marks |
| **Rubric 2** | Identification of the probe configuration flaw leading to pool instability | 3 Marks |
| **Rubric 3** | Formulation of balanced health check tuning parameters to eliminate flapping | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
