# Storage Lab: Enterprise LVM Volume Extension Under Live I/O Load with Rollback SOP

Duration : 90 Min.

## Scenario
A production enterprise cluster volume `/dev/vg_enterprise/lv_transactions` (mounted at `/opt/transactions`) is at 96% capacity. An additional raw LUN `/dev/sdc` (100 GB) has been provisioned by the SAN administrator. The engineer must inspect `lvm_cluster_extension.log`, execute a zero-downtime volume extension: initialize `/dev/sdc` as a Physical Volume (`pvcreate`), add it to Volume Group `vg_enterprise` (`vgextend`), extend the Logical Volume `lv_transactions` by 50 GB (`lvextend -L +50G`), expand the filesystem online, leave the remaining 50 GB in the VG as an emergency reserve, and formulate change-control verification in `lvm_extension_signoff.json`.

## Task Objectives

Perform the following enterprise LVM volume extension tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`lvm_cluster_extension.log`**: Raw system execution log documenting SAN LUN provisioning, pvcreate, vgextend, lvextend +50G, and online filesystem growth under live I/O.
> - **`lvm_extension_signoff.json`**: Starter change-control signoff template with `TODO_*` placeholders.

1. Review `lvm_cluster_extension.log` to record baseline LVM topology and verify pre-change capture (`baseline_topology_captured: YES`).
2. Initialize the provisioned raw LUN `/dev/sdc` using `pvcreate` with proper partition alignment.
3. Extend volume group `vg_enterprise` using `vgextend` to incorporate `/dev/sdc`.
4. Extend logical volume `lv_transactions` by targeted +50GB (`lvextend -L +50G`) rather than consuming all available space.
5. Expand the live filesystem online under continuous I/O load without transaction errors (`continuous_io_errors: NO`).
6. Verify that volume group `vg_enterprise` maintains 50 GB unallocated emergency headroom (`emergency_vg_reserve_free_gb: 50`).
7. Complete all change sign-off verification fields in `lvm_extension_signoff.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Review the pre-staged `lvm_cluster_extension.log` to analyze volume growth commands and emergency headroom reservation.
3. Update `lvm_extension_signoff.json` inside the `student_workspace/` directory, replacing all `TODO_*` placeholders with your verified findings and commands.
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
| **TC1** | Pre-change capture: baseline LVM topology and mount states accurately recorded in lvm_before.log | 3 Marks |
| **TC2** | Physical volume creation: pvcreate successfully initializes /dev/sdc with proper partition alignment | 3 Marks |
| **TC3** | Volume group expansion: vgextend incorporates /dev/sdc into vg_enterprise without disruptive locking | 3 Marks |
| **TC4** | Targeted LV growth: lvextend extends logical volume by exactly +50GB rather than consuming all space | 3 Marks |
| **TC5** | Filesystem expansion: filesystem grown online while continuous background write script runs without I/O error | 3 Marks |
| **TC6** | Emergency headroom: verification that volume group maintains unallocated extents for future emergency growth | 3 Marks |
| **TC7** | Change sign-off: lvm_extension_signoff.json documents before/after sizes, UUIDs, and verification checksums | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
