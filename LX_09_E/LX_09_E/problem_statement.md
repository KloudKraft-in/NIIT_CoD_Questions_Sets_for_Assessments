# Linux Lab: Network Host Status and Local Logging (Local VM)

Duration : 60 Min.

## Scenario

As a Network Operations Engineer, you are validating local network interfaces on a newly provisioned Linux server. You must perform basic networking verification checks by testing the local loopback interface and capturing the system hostname for local diagnostics.

## Task Objectives

Perform the following actions on your local Linux system:

### 1. Environment Verification
- Ensure the local VM environment is active under your default home directory (`/home/ubuntu`).

### 2. Loopback Interface Ping Check
- Ping the local loopback interface (`127.0.0.1`) with **exactly 4 packets**.
- Redirect/save the ping output summary to a file named `/home/ubuntu/ping_local.log`.

### 3. System Hostname Extraction
- Retrieve the system hostname using command-line utilities (e.g. `hostname`).
- Write the hostname string as the single line inside a new file named `/home/ubuntu/hostname_info.txt`.

### 4. Output Validation
- Ensure both output log files exist in `/home/ubuntu/` and contain non-empty diagnostic data.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 0 Marks |
| **TC2**   | Ping log `/home/ubuntu/ping_local.log` created | 2 Marks |
| **TC3**   | Ping log contains 4 packet transmission summary details | 2 Marks |
| **TC4**   | Hostname file `/home/ubuntu/hostname_info.txt` created | 3 Marks |
| **TC5**   | Hostname file contains valid system hostname | 3 Marks |

**Total Score: 10 Marks**
