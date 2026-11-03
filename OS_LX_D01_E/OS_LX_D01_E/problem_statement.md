# Linux Lab: Directory Navigation & System Path Hierarchy Setup (Local VM)

Duration : 30 Min.

## Scenario

A system administrator needs to prepare a standardized application workspace on an enterprise Linux server. You must create a nested application directory hierarchy, configure dotfile directories for hidden configuration files, and verify absolute path navigation.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Environment Verification

- Ensure the local Linux environment is active and your home directory (`~`) is reachable.

### 2. Directory Hierarchy Creation

- Create a nested directory structure inside your home directory: `~/app_env/config`, `~/app_env/logs`, and `~/app_env/.secret_keys`.

### 3. File Placement and Verification Script

- Create an empty configuration file named `app.conf` inside `~/app_env/config/`.
- Create an empty authentication key file named `auth.key` inside `~/app_env/.secret_keys/`.
- Create an executable verification shell script named `path_check.sh` inside your home directory (`~/path_check.sh`) or `~/app_env/` that outputs the absolute path of `app.conf` and the total count of hidden files in `~/app_env/`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                                                     | Marks   |
| ------------- | ----------------------------------------------------------------------------------------------- | ------- |
| **TC1** | Environment verification: local Linux environment active and home directory reachable           | 0 Marks |
| **TC2** | Directory hierarchy creation: verify creation of app_env/config, app_env/logs, and .secret_keys | 5 Marks |
| **TC3** | File placement and verification script: app.conf, auth.key, and path_check.sh execution         | 5 Marks |

**Total Score: 10 Marks**
