# Storage Lab: Multi-Alert Queue Triage & Failure Category Classification

Duration : 30 Min.

## Scenario
A storage support queue receives four raw alert payloads within a 15-minute window: (1) Alert A: 'Filesystem /data exceeded 95% threshold', (2) Alert B: 'VolumeQueueLength sustained > 32 for 10m on vol-0a1b2c', (3) Alert C: 'NFS server 10.0.4.5 not responding, RPC timed out', and (4) Alert D: 'Backup target snapshot rate exceeded quota'. The engineer must parse the alert payloads, classify each failure category, determine immediate response urgency, and generate a prioritized action dispatch list.

## Task Objectives

Perform the following storage alert triage tasks inside your `student_workspace` directory:

> **Pre-Staged Files in `student_workspace/`:**
> - **`incoming_alerts.json`**: Four raw JSON storage alert payloads received from monitoring systems.
> - **`prioritized_alerts.json`**: Starter triage queue template with `TODO_*` placeholders.

1. Ingest and review the incoming alert payloads in `incoming_alerts.json`.
2. Classify each alert into its primary failure domain (such as Capacity, Saturation/Performance, Connectivity/Mount, or Data Protection).
3. Prioritize each incident according to standard operational urgency (P1 to P4).
4. Identify the appropriate operational runbook or SOP for each failure domain.
5. Populate the prioritized dispatch queue in `prioritized_alerts.json`.

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
| **TC1** | Alert parsing: accurately extract affected resource ID, metric name, and trigger value from incoming_alerts.json | 4 Marks |
| **TC2** | Domain classification: 100% correct failure domain mapping for capacity, latency, mount, and backup errors | 3 Marks |
| **TC3** | Dispatch list generation: prioritized_alerts.json matches required schema with appropriate ITIL priority and SOP references | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
