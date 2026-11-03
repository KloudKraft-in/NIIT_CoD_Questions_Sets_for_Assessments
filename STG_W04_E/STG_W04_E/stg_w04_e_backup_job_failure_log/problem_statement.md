# Storage Lab: Backup Job Failure Log Analysis & Target Capacity Remediation

Duration : 30 Min.

## Scenario
A nightly enterprise backup job 'BACKUP_VOL_APP01' failed at 02:30 AM with return code 1. The monitoring ticket contains only a generic error 'Backup execution terminated unexpectedly'. The engineer must inspect the detailed backup agent log at /var/log/backup_agent/job_20261020.log, extract the specific error message ('ERROR: Target storage pool /mnt/backup_repo out of space - 0 bytes free'), diagnose the root failure category, and draft an operational remediation ticket.

## Task Objectives

Perform the following backup failure log analysis tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`job_20261020.log`**: Raw backup agent log containing the fatal failure trace.
> - **`backup_failure_triage.json`**: Starter triage report with `TODO_*` placeholders.

1. Review `job_20261020.log` to isolate the specific failure trace, timestamp, and target storage repository.
2. Classify the incident into its primary failure category (Destination Full, Permission Denied, Source Lock, or Schedule Conflict).
3. Determine the required corrective actions to restore the backup chain before the next scheduled run.
4. Document your triage findings, root cause analysis, and remediation steps in `backup_failure_triage.json`.

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
| **TC1** | Log parsing: accurately locate the failure line and isolate the underlying operating system / storage error | 4 Marks |
| **TC2** | Category classification: correctly classify the failure as 'Destination Full / Target Repository Exhaustion' | 3 Marks |
| **TC3** | Remediation recommendation: backup_failure_triage.json details safe pruning of expired backups before re-running | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
