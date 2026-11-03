# Network Troubleshooting: Layer Isolation Triage — The Silent Checkout Page

Duration : 30 Min.

## Scenario

A client calls the support desk stating: 'Our online checkout page just doesn't load — it's definitely a network issue.' The customer-facing symptom is an empty browser window that hangs indefinitely before displaying a connection timeout. An inexperienced support technician immediately opens an escalated ticket to the enterprise network firewall team. The network engineer must review the reported symptom, inspect the captured browser error log, methodically reason through which TCP/IP layers (Physical, IP Network, Transport, Application) could plausibly produce this behavior, and rule out layers using symptom vocabulary before touching diagnostic tools.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `checkout_browser_error.log`: Browser network error log capturing HTTP navigation attempts and connection timeout telemetry.
- `network_triage_ticket.json`: Support incident ticket metadata containing client host network configuration and reported symptoms.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Analyze the incident details in `network_triage_ticket.json` and the captured network error log in `checkout_browser_error.log`.
3. Perform a systematic layer-by-layer isolation analysis across the TCP/IP stack (Physical/Link, Network, Transport, Application) to determine the exact layer where communication fails.
4. Provide technical justification ruling in or ruling out each layer based on the artifact evidence and error signatures.
5. Formulate the technical test sequence to pinpoint the root cause at the identified failing layer before taking remediation actions.
6. Record your complete triage analysis, layer mapping, and escalation/remediation strategy in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Systematic layer-by-layer analysis evaluating the TCP/IP stack against observed error signatures | 5 Marks |
| **Rubric 2** | Accurate layer isolation and formulation of a verified diagnostic test sequence | 5 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
