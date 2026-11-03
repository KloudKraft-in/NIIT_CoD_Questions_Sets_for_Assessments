# Linux Lab: System Specification Reporting and Search (Local VM)

Duration : 60 Min.

## Scenario

As a DevOps Engineer, you need to check the resources of your local VM (disk space utilization and memory utilization parameters), create a consolidated hardware specifications report file, and search system configuration tables for specific network resolving entries.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Environment Verification
- Ensure the local VM environment is running with your default home directory (`~`).

### 2. System Specifications Report

- Query the disk space utilization (`df -h`) and system memory usage details (`free` or `vmstat` command), and redirect the combined command output to be saved in a new file named `~/spec_report.txt`.

### 3. Log Keyword Search

- Search for the exact keyword `nameserver` inside the DNS network configuration file `/etc/resolv.conf` and redirect the matching lines to be saved in a new file named `~/search_results.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 0 Marks |
| **TC2**   | System resources metrics written to `~/spec_report.txt` successfully | 5 Marks |
| **TC3**   | Network entries search saved to `~/search_results.txt` successfully | 5 Marks |

**Total Score: 10 Marks**
