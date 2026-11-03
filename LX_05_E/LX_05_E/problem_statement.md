# Linux Lab: File Copying and Executable Permissions (Local VM)

Duration : 60 Min.

## Scenario

As a systems administrator, you are tasked with copying an important configuration file from the system folder to your local user workspace and configuring its permission levels so that it can be executed safely by system utilities.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Environment Verification
- Ensure the local VM environment is running with your default home directory (`~`).

### 2. File Copy Operation

- Copy the system hosts configuration file located at `/etc/hosts` into your home directory (`~/`) and name the copied file `hosts_copy.txt`.

### 3. Permission Configuration

- Modify the file permissions of `~/hosts_copy.txt` to make it executable for all users (owner, group, and others), which corresponds to the octal permission mode `755` (`rwxr-xr-x`).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 0 Marks |
| **TC2**   | File copied to `~/hosts_copy.txt` successfully | 5 Marks |
| **TC3**   | Permissions set to `755` successfully | 5 Marks |

**Total Score: 10 Marks**
