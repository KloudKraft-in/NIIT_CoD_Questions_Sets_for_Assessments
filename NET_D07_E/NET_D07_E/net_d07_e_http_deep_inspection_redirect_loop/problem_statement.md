# Network Troubleshooting: HTTP Deep Inspection & Redirect Loops

Duration : 30 Min.

## Scenario

Users navigating to the corporate client portal `https://portal.enterprise.com/login` report that their browser displays 'ERR_TOO_MANY_REDIRECTS' and fails to open. An operations engineer captured a full verbose trace using `curl -ivL`. The trace reveals an infinite redirect loop bouncing between HTTP and HTTPS. The engineer must analyze the captured curl trace and reverse proxy configuration to identify the underlying cause of the redirection loop between the proxy and backend, and formulate the fix.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `curl_verbose_trace.log`: Verbose curl HTTP request trace documenting redirection headers and round trips.
- `nginx_reverse_proxy.conf`: NGINX reverse proxy server block and upstream proxy configuration.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Inspect `curl_verbose_trace.log` and `nginx_reverse_proxy.conf` in `student_workspace/`.
3. Trace the sequence of HTTP status codes, Location headers, and ports traversed during the connection attempts.
4. Analyze how the interaction between the edge proxy and backend application produces the infinite redirection loop.
5. Formulate the required reverse proxy configuration change to resolve the redirection loop.
6. Document your root cause analysis and exact configuration directives in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Detailed trace analysis of HTTP headers, status codes, and redirection flow | 4 Marks |
| **Rubric 2** | Accurate diagnosis of the proxy-backend communication mismatch causing the loop | 3 Marks |
| **Rubric 3** | Formulation of the correct reverse proxy configuration directives to eliminate the loop | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
