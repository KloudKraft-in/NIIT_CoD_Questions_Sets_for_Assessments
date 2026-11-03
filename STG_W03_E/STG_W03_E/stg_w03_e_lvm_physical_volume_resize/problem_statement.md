# Storage Lab: LVM Physical Volume Resize & Logical Volume Online Extension

Duration : 30 Min.

## Scenario
An underlying disk device `/dev/sdb` has been enlarged from 50 GB to 100 GB in the hypervisor/cloud console. However, the logical volume `/dev/vg_data/lv_app` mounted at `/data` still displays 50 GB. The administrator must inspect `lvm_pv_resize.log`, resize the physical volume (`pvresize`), extend the logical volume to consume all newly available volume group space (`lvextend`), grow the EXT4 filesystem online without unmounting `/data` (`resize2fs`), and record the expansion metrics in `lvm_resize_report.json`.

## Task Objectives

Perform the following LVM volume extension tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`lvm_pv_resize.log`**: Raw system execution log documenting disk expansion, pvresize, vgs metadata, lvextend, and resize2fs traces.
> - **`lvm_resize_report.json`**: Starter LVM online extension report with `TODO_*` placeholders.

1. Review `lvm_pv_resize.log` to inspect the underlying block device `/dev/sdb` and detect the newly expanded physical disk capacity (100 GB vs 50 GB).
2. Update the LVM metadata via `pvresize` so the physical volume and volume group `vg_data` recognize the unallocated space (100 GB).
3. Extend the logical volume `/dev/vg_data/lv_app` to consume 100% of the newly available volume group extents (`lvextend -l +100%FREE`).
4. Grow the live filesystem online (`resize2fs`) without unmounting the volume or interrupting service operations (`data_loss_experienced: NO`).
5. Record your executed commands, detected capacities, and resize completion status in `lvm_resize_report.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Review the pre-staged `lvm_pv_resize.log` to inspect physical volume expansion, volume group extents, and filesystem growth steps.
3. Update `lvm_resize_report.json` inside the `student_workspace/` directory, replacing all `TODO_*` placeholders with your verified configuration values.
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
| **TC1** | PV resize: pvresize successfully detects expanded underlying block device capacity | 2 Marks |
| **TC2** | VG metadata: volume group free extents updated and verified via vgs | 2 Marks |
| **TC3** | LV extension: logical volume extended to take 100% of newly available extents | 3 Marks |
| **TC4** | Filesystem growth: resize2fs completes online with zero data loss and df confirms 100GB usable space | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
