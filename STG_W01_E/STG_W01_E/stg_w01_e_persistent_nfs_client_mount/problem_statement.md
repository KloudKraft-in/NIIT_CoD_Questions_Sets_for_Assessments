# Storage Lab: Persistent NFS Client Mount & /etc/fstab Configuration

Duration : 30 Min.

## Scenario
An application node must mount a shared NFS export (`192.168.10.50:/srv/nfs/shared`) onto local mount directory `/mnt/app_shared`. The mount must persist across server reboots without causing the host to hang during boot if network connectivity is delayed. The administrator must inspect `nfs_mount_setup.log`, create the mount point with proper permissions (`0755`), configure a compliant `/etc/fstab` entry with critical network safety options (`_netdev`, `nofail`), verify the active mount and write operations, and record the configuration in `nfs_mount_report.json`.

## Task Objectives

Perform the following network filesystem administration tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`nfs_mount_setup.log`**: Raw system execution log documenting mount point setup, fstab entry, mount execution, and verification traces.
> - **`nfs_mount_report.json`**: Starter NFS mount configuration report with `TODO_*` placeholders.

1. Review `nfs_mount_setup.log` and verify the local mount point directory `/mnt/app_shared` with proper ownership and permission attributes (e.g., `0755`).
2. Configure a persistent mount entry for remote NFS export `192.168.10.50:/srv/nfs/shared` in `/etc/fstab` using filesystem type `nfs` (or `nfs4`).
3. Apply standard network safety mount options including `_netdev` and `nofail` so the host boots reliably without hanging if network connectivity is delayed.
4. Execute the mount and verify active filesystem reachability and write access inside `/mnt/app_shared`.
5. Record your mount point attributes, fstab configuration line, and verification results in `nfs_mount_report.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Review the pre-staged `nfs_mount_setup.log` to inspect mount parameters, permissions, and network safety options.
3. Update `nfs_mount_report.json` inside the `student_workspace/` directory, replacing all `TODO_*` placeholders with your verified configuration values.
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
| **TC1** | Mount point setup: directory /mnt/app_shared exists with proper ownership and permission attributes | 3 Marks |
| **TC2** | fstab syntax: /etc/fstab contains valid entry with critical network safety options (_netdev, nofail) | 4 Marks |
| **TC3** | Mount verification: mount command confirms active mount and test file creation succeeds inside /mnt/app_shared | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
