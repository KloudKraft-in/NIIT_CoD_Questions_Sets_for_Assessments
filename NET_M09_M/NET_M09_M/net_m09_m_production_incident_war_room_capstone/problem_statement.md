# Network Troubleshooting: Production Incident War-Room Multi-Layer Forensics

Duration : 60 Min.

## Scenario

During peak black-friday traffic, an enterprise payment cluster experiences a catastrophic outage. Multiple cascading symptoms appear simultaneously: (1) Core aggregation switches log LACP EtherChannel link flapping on the primary uplink; (2) DNS servers experience query timeouts during failover; (3) Application nodes accumulate 40,000 sockets in CLOSE_WAIT; and (4) The frontend load balancer drops 80% of client transactions with HTTP 502/504 errors. You are designated the Incident Commander in the Emergency War Room. You must synthesize the chronological incident logs, perform root cause analysis across all layers, formulate immediate triage steps, and author the definitive Post-Incident Review (PIR).

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `alb_metrics.json`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `ss_socket_dump.txt`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `syslog_switch_flapping.log`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `war_room_master_incident_log.txt`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `war_room_incident_timeline.json`, `gateway_access_combined.log`, `conntrack_top_talkers.txt`, and `upstream_health_status.json` in `student_workspace/`.
3. Conduct an end-to-end multi-layer forensic analysis of the major production outage spanning network, transport, and application layers.
4. Correlate disparate telemetry sources across edge gateways, connection tables, and upstream service health metrics.
5. Differentiate primary trigger events from secondary downstream symptoms and cascading side effects.
6. Produce an executive summary, complete technical root cause analysis, timeline reconstruction, and preventative engineering roadmap in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Multi-layer forensic investigation integrating network, transport, and application telemetry | 3 Marks |
| **Rubric 2** | Accurate differentiation between root cause trigger and secondary cascade symptoms | 3 Marks |
| **Rubric 3** | Rigorous chronological timeline reconstruction of the major incident | 2 Marks |
| **Rubric 4** | Cross-system correlation of edge logs, connection tracking, and backend health status | 2 Marks |
| **Rubric 5** | Formulation of immediate operational stabilization and recovery procedures | 2 Marks |
| **Rubric 6** | Design of systemic architectural improvements to eliminate single points of failure | 2 Marks |
| **Rubric 7** | Development of early-warning observability metrics and synthetic health checks | 3 Marks |
| **Rubric 8** | Professional executive post-mortem and engineering corrective action plan | 3 Marks |

**Total Score: 20 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
