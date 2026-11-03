# Network Troubleshooting: Egress NAT & Firewall Whitelist Triage

Duration : 30 Min.

## Scenario

Users in the EMEA regional office report that they cannot access the global procurement portal, while users in APAC and Americas access the portal without issue. An infrastructure engineer is provided with an enterprise network topology and firewall rule export. The engineer must inspect the artifacts, identify how Source NAT (SNAT) translations interact with the central ingress firewall whitelist, and specify the required firewall rule update.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `emea_connection_drop.log`: Firewall drop event log recording blocked egress connection attempts.
- `firewall_rules.csv`: Central firewall access control list and policy rules for outbound egress traffic.
- `network_topology.json`: Enterprise network topology mapping regional offices, NAT gateways, and firewall boundaries.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Inspect `network_topology.json`, `firewall_rules.csv`, and `emea_connection_drop.log` in `student_workspace/`.
3. Trace the outbound traffic path from internal client networks through regional egress NAT gateways to the external destination.
4. Compare the flow parameters between succeeding and failing regions to identify the root cause of the traffic rejection.
5. Formulate the required firewall rule modification or configuration change to restore connectivity for the affected region.
6. Document your path analysis, root cause evidence, and change request details in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Comparative path analysis identifying the discrepancy between regional traffic flows | 4 Marks |
| **Rubric 2** | Accurate identification of the firewall and NAT policy root cause from logs | 3 Marks |
| **Rubric 3** | Formulation of a complete, compliant change request to restore connectivity | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
