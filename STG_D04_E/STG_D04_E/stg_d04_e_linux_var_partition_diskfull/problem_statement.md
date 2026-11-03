# Storage Lab: Linux /var Partition Disk-Full SOP Execution & Safe Log Cleanup

Duration : 30 Min.

## Scenario

A production application server has raised a P2 alert: '/var filesystem at 98% utilization'. Application logging has paused due to out-of-space errors. The administrator must log into the host, identify the largest directories and files consuming space under /var/log, execute safe, change-controlled log cleanup (compressing uncompressed historical logs, purging rotated archives older than 30 days), and strictly avoid deleting open, active log files.

## Task Objectives

Perform the following storage administrative and diagnostic tasks:

> **Pre-Staged Files in `student_workspace/`:**
>
> - **`cleanup_report.json`**: Starter cleanup summary report with `TODO_*` placeholders.

1. Investigate the filesystem capacity crisis and identify the directories and files consuming excessive space under `/var/log`.
2. Safely perform change-controlled log cleanup by compressing older uncompressed logs and purging obsolete archives past retention policy.
3. Ensure that active log files currently held open by running system daemons are preserved without disruption.
4. Verify that filesystem utilization on `/var` drops below 75%.
5. Record your capacity restoration metrics and freed megabytes in `cleanup_report.json`.

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

| Test Case     | Requirement                                                                                                           | Marks   |
| ------------- | --------------------------------------------------------------------------------------------------------------------- | ------- |
| **TC1** | Identification of space hogs: script or command output correctly isolates the specific offending log directories      | 4 Marks |
| **TC2** | Safe cleanup execution: historical archives compressed/purged while active process file descriptors remain undamaged  | 3 Marks |
| **TC3** | Threshold recovery: verify /var partition utilization is below 75% and cleanup_report.json documents exact freed bytes | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
