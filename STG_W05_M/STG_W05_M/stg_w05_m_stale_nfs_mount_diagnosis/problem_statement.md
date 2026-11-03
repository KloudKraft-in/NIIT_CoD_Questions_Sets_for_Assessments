# Storage Lab: Stale NFS Mount Diagnosis & NetApp ONTAP SVM Export Policy Triage

Duration : 60 Min.

## Scenario
Following an enterprise network migration, an application server reports 'ESTALE (Stale file handle)' whenever accessing `/mnt/netapp_shared`. The share is hosted on a NetApp ONTAP Storage Virtual Machine (SVM). Running `ls /mnt/netapp_shared` hangs indefinitely. The engineer must inspect the pre-staged incident log (`nfs_stale_incident.log`), diagnose the stale mount, identify processes holding open file descriptors with `fuser`/`lsof`, perform a safe lazy unmount (`umount -l`), discover from the NetApp export policy dump that the client's new IP subnet (`192.168.20.0/24`) was missing from the export policy rule, formulate the remediation rule, remount successfully, and document the triage metrics in `stale_nfs_report.json`.

## Task Objectives

Perform the following stale NFS mount recovery and NetApp triage tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`nfs_stale_incident.log`**: Raw system and kernel trace documenting the stale mount, lock diagnosis, lazy unmount, NetApp export policy dump, and remount logs.
> - **`stale_nfs_report.json`**: Starter stale mount diagnostic report with `TODO_*` placeholders.

1. Review `nfs_stale_incident.log` to diagnose the stale mount state on `/mnt/netapp_shared`, extract the `ESTALE` error code, and identify processes holding locks using `fuser` or `lsof`.
2. Determine and verify the safe detach/unmount command using lazy unmount (`umount -l`) without causing kernel lockup or requiring a host reboot (`orphaned_kernel_states_avoided: YES`).
3. Analyze the NetApp export policy section in `nfs_stale_incident.log` to identify the rule mismatch (`192.168.20.0/24`) causing access denial and specify the exact remediation rule.
4. Document the remount command (`mount -t nfs -o vers=4.1 ...`), verify active read/write transaction completion, and set recovery status to `SUCCESS`.
5. Record your diagnosed error code, safe unmount command, root cause subnet, remediation rule, and recovery status in `stale_nfs_report.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Review the pre-staged `nfs_stale_incident.log` to analyze the failure trace, locking processes, and export policy rules.
3. Update `stale_nfs_report.json` inside the `student_workspace/` directory, replacing all `TODO_*` placeholders with your verified findings and commands.
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
| **TC1** | Stale mount identification: accurately diagnose ESTALE error condition and identify processes holding locks | 5 Marks |
| **TC2** | Safe unmount execution: successfully unmount the hung share using umount -l without leaving orphaned kernel states | 5 Marks |
| **TC3** | NetApp export policy analysis: correctly identify the missing client IP in export policy dump as root cause | 5 Marks |
| **TC4** | Successful recovery: remount share successfully and verify read/write transaction completion | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
