# Network Troubleshooting: Reverse Proxy CORS & Security Header Inspection

Duration : 45 Min.

## Scenario

A single-page React application hosted on `https://app.enterprise.com` fails to invoke backend API endpoints at `https://api.enterprise.com/v1/users`, with browser consoles logging: 'Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource (Reason: CORS header Access-Control-Allow-Origin missing)'. An engineer captured a `curl -iv -X OPTIONS` pre-flight trace and the reverse proxy configuration. The network engineer must inspect these artifacts, diagnose the missing CORS headers, and specify the NGINX gateway header injection directives.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `browser_cors_console.log`: Browser developer tools console log capturing Cross-Origin Resource Sharing errors.
- `curl_cors_options_trace.log`: Curl verbose HTTP OPTIONS preflight request and response trace.
- `nginx_api_gateway.conf`: API gateway NGINX configuration file defining upstream routing and headers.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `curl_cors_options_trace.log`, `nginx_api_gateway.conf`, and `browser_cors_console.log` in `student_workspace/`.
3. Analyze the HTTP preflight handshake and explain the cross-origin security boundaries enforced by web browsers.
4. Evaluate the headers returned in the gateway trace against standard cross-origin resource sharing requirements.
5. Determine the exact missing header directives causing browser preflight requests to fail.
6. Provide the complete reverse proxy configuration block required to handle preflight requests and inject required CORS headers in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Accurate technical evaluation of browser CORS preflight mechanisms and HTTP header flows | 4 Marks |
| **Rubric 2** | Precise identification of missing response headers and proxy configuration gaps | 3 Marks |
| **Rubric 3** | Formulation of a fully compliant gateway configuration block resolving cross-origin errors | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
