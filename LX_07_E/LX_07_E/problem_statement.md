# Linux Lab: User and Directory Navigation (Local VM)

Duration : 60 Min.

## Scenario

As a Junior System Administrator in an IT operations team, you are tasked with setting up a temporary backup workspace in the system `/var/tmp/` directory to manage log files. This involves utilizing Linux directory navigation, file creation, moving, and renaming operations.

## Task Objectives

Perform the following actions on your local Linux system:

### 1. Environment Verification
- Ensure the local VM environment is running with standard user access.

### 2. Backup Workspace Directory Creation
- Create a directory named `backup_workspace` inside the `/var/tmp/` directory (`/var/tmp/backup_workspace`).

### 3. Initial Log File Creation
- Create an empty file named `meta_log.txt` inside `/var/tmp/backup_workspace/`.

### 4. File Migration and Renaming
- Move the file `meta_log.txt` from `/var/tmp/backup_workspace/` to your home directory (`/home/ubuntu/`).
- Rename the file during or after the move to `meta_backup.log` so that its absolute path is `/home/ubuntu/meta_backup.log`.

### 5. Workspace Cleanup Verification
- Verify that `meta_log.txt` no longer exists inside `/var/tmp/backup_workspace/`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 0 Marks |
| **TC2**   | Backup workspace directory (`/var/tmp/backup_workspace/`) created successfully | 2 Marks |
| **TC3**   | Initial log file (`meta_log.txt`) created inside backup workspace | 2 Marks |
| **TC4**   | File moved to `/home/ubuntu/` and renamed to `meta_backup.log` | 3 Marks |
| **TC5**   | File `meta_log.txt` correctly cleaned up from backup workspace | 3 Marks |

**Total Score: 10 Marks**
