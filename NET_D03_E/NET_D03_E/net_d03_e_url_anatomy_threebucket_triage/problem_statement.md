# Network Troubleshooting: URL Anatomy & Three-Bucket Triage

Duration : 30 Min.

## Scenario

A high-priority incident ticket arrives with the title: 'The API is down! Customers are blocked!' The ticket contains only a single URL: 'https://api-orders.internal.corp:8443/v2/orders?status=pending'. The support analyst must decompose the URL into its constituent architectural elements, inspect the pre-gathered diagnostic command outputs, and execute a structured three-bucket triage model to determine whether the failure is Bucket 1: DNS failure, Bucket 2: Connectivity failure, or Bucket 3: Application-layer failure.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `api_incident_ticket.txt`: Incident dispatch ticket describing partner API connectivity failures.
- `curl_api_error.log`: HTTP client execution trace and server response headers from the API call.
- `nc_port_test.log`: Layer 4 TCP socket connection probe results for the target API port.
- `nslookup_api_output.txt`: DNS query results for the external partner API hostname.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Inspect `api_incident_ticket.txt`, `nslookup_api_output.txt`, `nc_port_test.log`, and `curl_api_error.log` in `student_workspace/`.
3. Deconstruct the target URL into its architectural components (protocol scheme, hostname, port, path, parameters).
4. Apply the Three-Bucket triage model (DNS vs Connectivity vs Application) by analyzing the evidence from the diagnostic tool outputs.
5. Determine the exact failure domain and specific error cause responsible for the transaction failure.
6. Formulate an actionable ticket update and dispatch recommendation in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Accurate architectural breakdown and component identification of the target URL | 4 Marks |
| **Rubric 2** | Rigorous execution of the Three-Bucket decision tree using captured tool logs | 3 Marks |
| **Rubric 3** | Correct failure domain classification and actionable ticket routing recommendation | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
