# Linux Lab: Secure Directory Layout and Ownership Audit (Local VM)

Duration : 60 Min.

## Scenario

As a Security Systems Administrator, you are tasked with setting up a secure application data workspace containing configuration files and secret keys. You must configure ownership and permissions such that only the `root` owner has write access, while the application group (`ubuntu`) can execute/read, and other standard users have no access whatsoever. Additionally, you must package the configuration directory into a compressed archive for recovery purposes.

## Task Objectives

Perform the following actions on your local Linux system:

### 1. Environment Verification
- Ensure the local VM environment is active under your default home directory (`/home/ubuntu`).

### 2. Directory Layout & Initial File Setup
- Create a directory named `/home/ubuntu/app_data/`.
- Inside `/home/ubuntu/app_data/`, create two blank files: `config_dev.conf` and `database.key`.

### 3. Ownership Management
- Recursively change the ownership of `/home/ubuntu/app_data/` and all files inside it so that the owner user is `root` and the owner group is `ubuntu` (`root:ubuntu`).

### 4. Permission Hardening
Modify permissions for the directory and individual files as follows:
- **Directory `/home/ubuntu/app_data/`**: Set permissions to exactly `755` (`rwxr-xr-x`).
- **File `config_dev.conf`**: Set permissions to exactly `644` (`rw-r--r--`).
- **File `database.key`**: Set permissions to exactly `400` (`r--------`).

### 5. Compressed Backup Archive
- Package the entire `/home/ubuntu/app_data/` directory into a compressed gzip tar archive located at `/home/ubuntu/app_backup.tar.gz`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 0 Marks |
| **TC2**   | Application directory `/home/ubuntu/app_data/` created with mode `755` | 3 Marks |
| **TC3**   | Target files `config_dev.conf` and `database.key` created | 3 Marks |
| **TC4**   | Ownership recursively assigned to `root:ubuntu` | 3 Marks |
| **TC5**   | File `config_dev.conf` permissions set to `644` (`rw-r--r--`) | 3 Marks |
| **TC6**   | File `database.key` permissions set to `400` (`r--------`) | 4 Marks |
| **TC7**   | Compressed archive `/home/ubuntu/app_backup.tar.gz` created successfully | 4 Marks |

**Total Score: 20 Marks**
