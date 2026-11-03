# Network Troubleshooting: Load Balancer Health Probe Mismatch

Duration : 30 Min.

## Scenario

An Application Load Balancer (ALB) monitoring dashboard fires a critical alert: '50% Backend Capacity Lost — 2 of 4 targets Unhealthy'. User traffic is now concentrated on the remaining two instances, causing CPU saturation. An inexperienced operator proposes rebooting the two unhealthy application instances. The network engineer inspects the ALB target health logs and backend access logs to determine if the servers are truly down or if the health check probe is misconfigured.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `alb_target_health.json`: Application Load Balancer target group health check status and failure reasons.
- `backend_access.log`: Backend application HTTP access logs capturing probe requests and status codes.
- `release_notes_v2.4.txt`: Application deployment changelog and health endpoint release notes.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `alb_target_health.json`, `backend_access.log`, and `release_notes_v2.4.txt` in `student_workspace/`.
3. Analyze the health check status codes, error descriptions, and target states reported by the load balancer.
4. Correlate the load balancer health check requests against the backend application access logs.
5. Determine why the backend instances failed health checks despite the application process running.
6. Formulate the load balancer configuration remediation to bring the target group back into healthy service in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Detailed correlation between load balancer probe metrics and backend application logs | 4 Marks |
| **Rubric 2** | Accurate root cause determination distinguishing service failure from probe misconfiguration | 3 Marks |
| **Rubric 3** | Actionable remediation plan with precise target group parameters to restore traffic | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
