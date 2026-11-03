# Storage Lab: Catastrophic Partition Saturation & Emergency Multi-Tier Space Reclamation

Duration : 90 Min.

## Scenario
A mission-critical transaction server has hit 100% disk usage on the root filesystem (/). Core utilities are failing with 'No space left on device'. Standard 'rm' commands have been executed by an inexperienced technician on large log files, yet 'df -h' still displays 100% because the deleted files are still held open by running application processes (lsof +L1). The engineer must perform emergency space recovery: identify deleted-yet-open file descriptors, truncate open files cleanly without crashing the daemon, purge unneeded Linux core dumps in /var/lib/systemd/coredump, vacuum the systemd journal, and restore normal operation.

## Task Objectives

Perform the following emergency storage space reclamation tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`disk_saturation_emergency.log`**: System incident log capturing df outputs, lsof unlinked file descriptor diagnostics, and multi-tier space reclamation commands.
> - **`emergency_reclamation.json`**: Starter reclamation summary template with `TODO_*` placeholders.

1. Diagnose the 100% root filesystem saturation condition and determine why standard deletion commands failed to release space using `disk_saturation_emergency.log`.
2. Locate unlinked files held open by running application processes and safely zero the open descriptors without killing the daemons.
3. Purge obsolete crash dumps and vacuum systemd journal logs to restore operating headroom.
4. Verify that filesystem utilization drops below 70% and document recovered capacity in `emergency_reclamation.json`.

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
| **TC1** | 100% capacity diagnosis: confirm filesystem saturation and explain discrepancy between du and df | 3 Marks |
| **TC2** | Open descriptor identification: lsof accurately identifies the specific PIDs and FDs holding deleted logs | 3 Marks |
| **TC3** | Safe zeroing of descriptors: open descriptors truncated via /proc filesystem without process crash or data loss | 3 Marks |
| **TC4** | Core dump purging: obsolete crash dumps safely purged from /var/lib/systemd/coredump | 3 Marks |
| **TC5** | Journal vacuuming: journalctl --vacuum-size executed correctly reducing systemd journal footprints | 3 Marks |
| **TC6** | Package cache cleanup: system package manager cache cleared cleanly without removing installed packages | 3 Marks |
| **TC7** | Headroom recovery: df confirms root partition usage < 70% and emergency_reclamation.json is fully compiled | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
