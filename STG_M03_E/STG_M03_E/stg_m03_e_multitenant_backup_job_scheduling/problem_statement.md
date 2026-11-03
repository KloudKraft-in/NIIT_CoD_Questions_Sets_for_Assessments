# Storage Lab: Multi-Tenant Backup Job Scheduling & Lock Conflict Resolution

Duration : 30 Min.

## Scenario
Two automated backup scripts (a database snapshot script and a file-level archive script) run simultaneously at 01:00 AM, both attempting to lock the shared underlying storage volume /dev/vg_app/lv_data. The database snapshot fails with 'ERROR: Volume lock already acquired by another process'. The engineer must analyze the lock conflict, reschedule the jobs into sequential, non-overlapping windows with sufficient buffer, and implement lock-file verification.

## Task Objectives

Perform the following backup schedule optimization and concurrency control tasks inside your `student_workspace` directory:

> **Pre-Staged Files in `student_workspace/`:**
> - **`backup_durations.log`**: Historical backup execution duration logs.
> - **`backup_schedule_report.json`**: Optimization report template with `TODO_*` placeholders.

1. Review `backup_durations.log` to identify schedule overlap and lock collisions between concurrent backup jobs.
2. Re-architect the backup cron schedules into sequential, non-overlapping windows with adequate safety buffers.
3. Formulate an advisory file locking mechanism using `flock` and define lock file parameters to prevent concurrent job collisions.
4. Verify that concurrent execution attempts handle lock contention gracefully and exit with clean warning handling.
5. Record your schedule analysis, recommended cron expressions, buffer times, and lock verification in `backup_schedule_report.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Review the duration logs and analyze the concurrency lock conflict.
3. Complete the fields in `backup_schedule_report.json` inside the `student_workspace` directory.
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
| **TC1** | Schedule conflict detection: accurately identify the 01:00 AM race condition between snapshot and archive jobs | 3 Marks |
| **TC2** | Window optimization: cron schedule adjusted to separate jobs based on observed completion times | 2 Marks |
| **TC3** | Advisory lock specification: flock advisory locking mechanism and lockfile path formulated to prevent concurrent collisions | 3 Marks |
| **TC4** | Verification test: verify concurrent lock contention behavior and validate clean exit with warning | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
