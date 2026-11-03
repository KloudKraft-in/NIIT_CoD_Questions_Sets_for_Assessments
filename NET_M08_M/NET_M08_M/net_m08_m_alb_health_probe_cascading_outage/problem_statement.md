# Network Troubleshooting: Application Load Balancer Health Probe Cascading Failure

Duration : 60 Min.

## Scenario

A 10-node application cluster behind an Application Load Balancer suffers a total collapse. Initially, one node experienced high load and delayed its health check response by 5 seconds, causing the ALB to mark it 'Unhealthy'. The ALB immediately diverted 100% of that node's traffic across the remaining 9 nodes. This extra load pushed a second node into delay, marking it Unhealthy. Within 4 minutes, all 10 nodes were sequentially marked Unhealthy by the ALB, resulting in a total service outage (HTTP 503) even though all 10 nodes were operational. The engineer must analyze the ALB incident timeline, backend thread pool metrics, and health probe design to halt cascading outages and re-architect the health probe.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `alb_cascade_event_timeline.json`: Timeline of load balancer health checks, node evictions, and failure events.
- `backend_thread_pools.csv`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `probe_latency_log.txt`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `alb_cascade_event_timeline.json`, `target_group_thresholds.conf`, and `container_oom_events.log` in `student_workspace/`.
3. Reconstruct the chronological sequence of events leading from initial node degradation to total pool unavailability.
4. Analyze the relationship between health check probe frequency, backend load, and instance eviction triggers.
5. Explain the 'thundering herd' and cascading failure dynamics that caused surviving nodes to collapse under redistributed traffic.
6. Formulate a resilient health check, auto-scaling, and load balancer configuration to prevent cascading outages in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Chronological incident reconstruction correlating health probe evictions with service collapse | 3 Marks |
| **Rubric 2** | In-depth technical analysis of cascading failure and traffic redistribution dynamics | 3 Marks |
| **Rubric 3** | Evaluation of health check probe impact on backend system resources | 2 Marks |
| **Rubric 4** | Identification of misconfigured thresholds and timeout margins triggering false positives | 2 Marks |
| **Rubric 5** | Formulation of hardened health check parameters with exponential backoff or jitter | 2 Marks |
| **Rubric 6** | Design of graceful degradation, circuit breaker, and rate-limiting protections | 2 Marks |
| **Rubric 7** | Specification of auto-scaling policies resilient against rapid instance flailing | 3 Marks |
| **Rubric 8** | Complete architectural post-mortem and site reliability engineering runbook | 3 Marks |

**Total Score: 20 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
