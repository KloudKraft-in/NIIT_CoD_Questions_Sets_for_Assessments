# Network Troubleshooting: Hybrid Cloud Asymmetric Routing & Stateful Firewall Drops

Duration : 60 Min.

## Scenario

Following an AWS hybrid cloud migration, database servers in a private VPC subnet (10.100.20.0/24) cannot communicate with on-premises mainframe services (10.20.0.0/16). Outbound TCP connections from the cloud initiate successfully, but sessions drop with connection timeouts. A network packet capture on the on-premises stateful firewall reveals that outbound SYN packets arrive via the AWS Direct Connect gateway, but the on-premises firewall drops returning SYN-ACK packets with 'Out of state / No matching session'. The engineer must analyze the routing tables, packet capture summary, and firewall logs to resolve the asymmetric routing loop.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `cloud_route_table.json`: Cloud VPC route table definitions and next-hop gateway configurations.
- `firewall_flow_logs.json`: Enterprise perimeter firewall flow logs capturing packet decisions and interfaces.
- `packet_capture_summary.txt`: Summary of packet capture traces showing bidirectional TCP connection handshakes.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `cloud_route_table.json`, `firewall_flow_logs.json`, and `packet_capture_summary.txt` in `student_workspace/`.
3. Map the end-to-end forward and reverse network paths between the cloud VPC and on-premises core infrastructure.
4. Analyze the packet capture and firewall flow logs to diagnose the reason for TCP connection failures between the environments.
5. Explain the mechanism by which stateful firewalls handle asymmetric traffic paths and out-of-sequence TCP packets.
6. Formulate an architectural routing and NAT remediation plan to establish symmetric pathing and restore stable hybrid connectivity in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Comprehensive bidirectional path mapping between cloud VPC and on-premises datacenter | 5 Marks |
| **Rubric 2** | Accurate technical diagnosis of stateful firewall drops resulting from asymmetric routing | 5 Marks |
| **Rubric 3** | Evaluation of architectural remediation options (routing alignment vs NAT vs state bypass) | 5 Marks |
| **Rubric 4** | Formulation of a verified routing table modification and deployment plan | 5 Marks |

**Total Score: 20 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
