# Storage Lab: Unresponsive Network Mount Clean Teardown & Process Remediation

Duration : 30 Min.

## Scenario
A remote network file share mounted at `/mnt/remote_nfs` has become completely unresponsive due to an abrupt storage cluster network outage. Any system commands such as `df -h` or `ls /mnt/remote_nfs` freeze indefinitely in uninterruptible sleep (D-state). The systems engineer must inspect `unresponsive_mount_incident.log`, safely detect the hung state using `timeout`, terminate stuck processes holding open file descriptors with `fuser -km`, perform a lazy unmount (`umount -l`) to detach the dead mount point without rebooting the host, verify `/proc/mounts`, and document all remediation actions in `unresponsive_mount_report.json`.

## Task Objectives

Perform the following unresponsive network mount remediation tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`unresponsive_mount_incident.log`**: Raw incident log documenting mount timeout, process lock detection, SIGKILL termination, and lazy unmount traces.
> - **`unresponsive_mount_report.json`**: Starter mount recovery report with `TODO_*` placeholders.

1. Review `unresponsive_mount_incident.log` to detect the frozen mount point `/mnt/remote_nfs` using `timeout` and capture the exit code (`124`) and mount status (`HUNG`).
2. Identify and terminate processes holding locks to the dead share using `fuser` with termination signal `SIGKILL` (`9`).
3. Safely detach the unresponsive filesystem using lazy unmount (`umount -l`) without causing system kernel hang.
4. Verify that `/mnt/remote_nfs` is completely removed from `/proc/mounts` and storage monitoring tools (`df -h`) operate normally without hanging (`storage_tools_responsive: YES`).
5. Document all commands, exit codes, and teardown metrics in `unresponsive_mount_report.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Review the pre-staged `unresponsive_mount_incident.log` to analyze the failure trace, timeout behavior, and process signals.
3. Update `unresponsive_mount_report.json` inside the `student_workspace/` directory, replacing all `TODO_*` placeholders with your verified findings and commands.
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
| **TC1** | Mount hung detection: timeout command detects mount freeze without causing diagnostic tool lockup | 3 Marks |
| **TC2** | Process termination: fuser cleanly signals processes in D-state holding descriptors to the dead share | 2 Marks |
| **TC3** | Lazy unmount execution: umount -l successfully detaches the unresponsive filesystem from directory tree | 3 Marks |
| **TC4** | State verification: /proc/mounts confirms removal and df operates normally without hanging | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
