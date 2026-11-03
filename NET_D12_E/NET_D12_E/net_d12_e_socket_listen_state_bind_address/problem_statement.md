# Network Troubleshooting: Socket Listen State & Interface Bind Address

Duration : 30 Min.

## Scenario

A mission-critical payment processing host is reported 'Down' by synthetic monitors. The application support team checks the server and reports: 'The payment process Java PID 4821 is running and using CPU, so the service is fine.' Yet remote clients cannot connect on port 8080. The network engineer captured `ss -tulpn` output and an external client connection log. The engineer must inspect these artifacts, identify the bind address anomaly, and formulate the remediation.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `application_config.properties`: Service deployment and network interface binding configuration.
- `external_connection_attempt.log`: Client-side connection attempt trace recording connection status.
- `ss_tulpn_capture.txt`: Linux socket statistics (`ss -tulpn`) capturing listening ports and bind addresses.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `ss_tulpn_capture.txt`, `external_connection_attempt.log`, and `application_config.properties` in `student_workspace/`.
3. Analyze the socket listening state, protocol, port, and bind address of the running service process.
4. Explain the network stack behavior and kernel response when external traffic attempts to reach a service bound to a specific local address.
5. Identify the root cause of the connection refusal and determine the required configuration update.
6. Document your technical analysis and configuration change in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Accurate interpretation of socket tables, listening states, and interface bind semantics | 4 Marks |
| **Rubric 2** | Technical explanation of kernel TCP response behavior for unexposed interfaces | 3 Marks |
| **Rubric 3** | Formulation of the exact configuration update required to enable external connectivity | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
