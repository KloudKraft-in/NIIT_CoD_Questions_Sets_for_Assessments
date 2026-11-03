# Linux Lab: Custom Configuration Copy and Permissions (Local VM)

Duration : 60 Min.

## Scenario

As a Systems Engineer, you are deploying a customized environment configuration script to a user space environment. You must copy the system-wide environment configuration file and modify access rights so that it is readable and writable strictly by the owner (`ubuntu`), and completely inaccessible to other users.

## Task Objectives

Perform the following actions on your local Linux system:

### 1. Environment Verification
- Ensure the local VM environment is active under your default home directory (`/home/ubuntu`).

### 2. Configuration File Deployment
- Copy the system environment configuration file located at `/etc/environment` to your home directory `/home/ubuntu/`.
- Save the copied file under the filename `env_local.txt` (so its absolute path is `/home/ubuntu/env_local.txt`).

### 3. File Content Preservation
- Ensure the contents of `/home/ubuntu/env_local.txt` match `/etc/environment`.

### 4. Permission Hardening
- Modify the access permissions of `/home/ubuntu/env_local.txt` to make it read and write only for the owner (`ubuntu`), with no read/write/execute permissions for group and others.
- The octal permission mode must be set to `600` (`rw-------`).

### 5. Ownership Verification
- Ensure the file owner is set to the current user (`ubuntu`).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 0 Marks |
| **TC2**   | Configuration file copied to `/home/ubuntu/env_local.txt` | 2 Marks |
| **TC3**   | File content matches system `/etc/environment` | 2 Marks |
| **TC4**   | Permissions hardened strictly to octal mode `600` (`rw-------`) | 3 Marks |
| **TC5**   | File ownership assigned to default user (`ubuntu`) | 3 Marks |

**Total Score: 10 Marks**
