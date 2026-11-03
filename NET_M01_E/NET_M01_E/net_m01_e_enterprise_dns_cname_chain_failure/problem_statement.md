# Network Troubleshooting: Enterprise DNS CNAME Chain & Zone Resolution Failure

Duration : 45 Min.

## Scenario

A high-visibility corporate campaign site `https://promo.enterprise.com` suddenly becomes unreachable for global users. Internal clients report `DNS_PROBE_FINISHED_NXDOMAIN`. An engineer captured a `dig +trace +stats` execution log, an authoritative DNS zone file excerpt, and client cache logs. The engineer must inspect these artifacts, identify the broken link in the CNAME chain, and specify the zone record remediation.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `dns_dig_trace.log`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `named_zone_file.db`: Pre-provisioned telemetry trace / configuration artifact for inspection.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `dns_cname_trace.txt`, `bind_named_cache.log`, and `zone_records.json` in `student_workspace/`.
3. Trace the full canonical name (CNAME) alias resolution chain from initial query to terminal record.
4. Analyze the DNS server cache and response codes to identify where resolution terminates or fails.
5. Determine the root cause of the query resolution failure and identify any violations of DNS protocol standards.
6. Formulate the required DNS zone record corrections and cache management commands in `student_workspace/triage_report.md`.

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
| **Rubric 1** | Systematic tracing of multi-tier DNS CNAME delegation chains and query responses | 3 Marks |
| **Rubric 2** | Accurate diagnosis of the zone configuration defect causing resolution failure | 3 Marks |
| **Rubric 3** | Technical explanation of DNS resolver caching behavior and TTL implications | 2 Marks |
| **Rubric 4** | Specification of exact zone record modifications and verification tests | 2 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
