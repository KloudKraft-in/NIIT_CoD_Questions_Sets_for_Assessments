# Storage Lab: Production Database Storage Latency Triage Across CloudWatch & Dynatrace

Duration : 90 Min.

## Scenario
A financial payment service reports that transaction response times spiked from 50 ms to 1,200 ms during peak processing hours. The application team blames the database server storage. The storage engineer is provided with CloudWatch metric extracts (VolumeReadTime, VolumeWriteTime, VolumeQueueLength, VolumeThroughputPercentage) and Dynatrace disk I/O metrics across the same 2-hour window. The engineer must correlate the time-series data, determine whether the latency spike originated in the storage subsystem (e.g., EBS burst balance exhaustion or provisioned IOPS throttling) or was driven by application-level locking.

## Task Objectives

Perform the following database storage latency root cause analysis tasks inside your `student_workspace` directory:

> **Pre-Staged Files in `student_workspace/`:**
> - **`database_latency_incident.log`**: Incident telemetry log capturing Dynatrace APM alerts, CloudWatch metric entries, and throttling events across the incident window.
> - **`storage_rca_report.json`**: Starter RCA report skeleton with `TODO_*` placeholders.

1. Ingest `database_latency_incident.log` to correlate time-series intervals where queue depths exceeded thresholds.
2. Calculate average per-I/O latency and determine whether IOPS or throughput hit provisioned volume baselines.
3. Determine whether the storage subsystem is responsible for application slowdowns or if application-level locking was the cause.
4. Formulate specific volume reconfiguration recommendations and author the incident report in `storage_rca_report.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Execute the required storage management commands, volume operations, or configuration edits.
3. If configuration files, backup manifests, or diagnostic reports are required, save them inside the `student_workspace` directory.
4. Verify your storage configurations locally by executing:
   ```bash
   python run.py
   ```
5. Once verified, return to the platform dashboard and click **"Run Tests"** / **"Full Eval"** to evaluate your score!

## Validation
Once your storage tasks are executed, return to the platform dashboard and click the **"Run Tests"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Time-series correlation: accurately match CloudWatch queue depth spikes to the application latency spike window | 3 Marks |
| **TC2** | Per-IO latency calculation: correctly calculate average read and write latencies in milliseconds | 3 Marks |
| **TC3** | Throttling identification: detect whether IOPS or Throughput reached 100% of provisioned volume limits | 3 Marks |
| **TC4** | EBS burst credit audit: evaluate burst balance depletion pattern on gp2 or baseline throttling on gp3 | 3 Marks |
| **TC5** | Root cause determination: convincingly substantiate whether storage subsystem caused the transaction delay | 3 Marks |
| **TC6** | Remediation blueprint: specify exact volume configuration modifications (e.g. modify-volume --iops --throughput) | 3 Marks |
| **TC7** | RCA documentation: storage_rca_report.json follows standard post-incident review format with charts/tables | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
