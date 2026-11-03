# Network Troubleshooting: Microservice DNS Resolution Latency & Search Domain Triage

Duration : 30 Min.

## Scenario

A Kubernetes worker node hosting backend payment services experiences recurring 5,000 ms API response delays. The developer insists the microservice code takes only 10 ms to compute results. The network engineer executed `dig +trace +stats` and inspected `/etc/resolv.conf`. The engineer discovers that the primary nameserver is offline, causing every new outbound request to wait for a 5-second timeout before falling back to the secondary nameserver. The engineer must document the latency escalation and formulate the resolver configuration fix.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `dns_query_perf.log`: DNS query performance and resolver response time log.
- `resolv_conf.txt`: System DNS resolver configuration (`/etc/resolv.conf`).
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `resolv_conf.txt` and `dns_query_perf.log` in `student_workspace/`.
3. Analyze the resolver query logs and identify the pattern of delays across configured nameservers.
4. Evaluate the resolver configuration parameters (nameservers, search domains, ndots) and explain how they influence query latency.
5. Determine the primary root cause responsible for the connection delay.
6. Provide the optimized resolver configuration and tuning directives in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Detailed analysis of DNS resolution timing, query sequences, and failover behavior | 4 Marks |
| **Rubric 2** | Accurate diagnosis of the resolver configuration flaw creating query latency spikes | 3 Marks |
| **Rubric 3** | Formulation of a hardened, optimized DNS resolver configuration | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
