# Storage Lab: End-to-End Cloud Block Volume Resize & XFS/EXT4 Filesystem Growth

Duration : 60 Min.

## Scenario
A cloud virtual machine has its attached block volume `/dev/nvme1n1` resized from 100 GB to 250 GB in the cloud control plane. However, the OS partition `/dev/nvme1n1p1` and its XFS filesystem mounted at `/var/lib/pgsql` still register 100 GB. The application database is actively running and cannot experience downtime. The engineer must inspect `cloud_volume_resize.log` to analyze the disk geometry discrepancy, use `growpart` to expand partition 1, use `xfs_growfs` to extend the XFS filesystem online, verify zero loss of running database transactions, and document the full execution sequence in `cloud_resize.json`.

## Task Objectives

Perform the following zero-downtime cloud block volume expansion tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`cloud_volume_resize.log`**: Raw cloud event, disk geometry trace (`lsblk`/`df`), growpart, and xfs_growfs execution log.
> - **`cloud_resize.json`**: Starter execution log with `TODO_*` placeholders.

1. Review `cloud_volume_resize.log` to inspect the enlarged cloud block device `/dev/nvme1n1` and identify the unallocated disk partition space (250 GB vs 100 GB).
2. Expand the active OS partition (`/dev/nvme1n1p1`) using `growpart` to consume the full available volume capacity without corrupting the partition table.
3. Extend the live XFS filesystem online using `xfs_growfs` while database I/O operations continue in the background.
4. Verify that the expanded filesystem capacity (~250 GB) is recognized via `df -hT` with uninterrupted database continuous writes (`database_io_interrupted: NO`), and document execution steps in `cloud_resize.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Review the pre-staged `cloud_volume_resize.log` to analyze the disk geometry discrepancy and volume expansion steps.
3. Update `cloud_resize.json` inside the `student_workspace/` directory, replacing all `TODO_*` placeholders with your verified parameters, tools, and results.
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
| **TC1** | Disk geometry inspection: correctly identify discrepancy between disk device size and partition size via lsblk | 5 Marks |
| **TC2** | Partition table extension: growpart successfully expands partition 1 without corrupting partition GUID table (GPT) | 5 Marks |
| **TC3** | Online filesystem expansion: xfs_growfs extends the live XFS filesystem online without requiring unmount | 5 Marks |
| **TC4** | Integrity & verification: database writes verified intact and df -hT confirms ~250 GB available space | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
