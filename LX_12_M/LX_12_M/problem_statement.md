# Linux Lab: Disk Telemetry and Socket Audit (Local VM)

Duration : 60 Min.

## Scenario

As an Infrastructure Security Analyst, you are tasked with performing system diagnostics and security audits on an Ubuntu Linux server. You must troubleshoot local disk space consumption, locate configuration files referencing loopback interfaces, and audit active listening network sockets to map exposed services.

## Task Objectives

Perform the following actions on your local Linux system using command-line utilities:

### 1. Environment Verification
- Ensure the local VM environment is active under your default home directory (`/home/ubuntu`).

### 2. Disk Space Consumption Analysis
- Analyze directory sizes of `/etc/` using `du -sh` (or equivalent disk usage command).
- Save the disk consumption summary of `/etc/` to `/home/ubuntu/etc_size.txt`.

### 3. Local IP Configuration Search
- Search recursively inside `/etc/` for any file containing the loopback IP string `"127.0.0.1"`.
- Save the list of absolute file paths (one per line) to `/home/ubuntu/local_ips.txt`.

### 4. Active Network Socket & Port Audit
- Query the system to find all active listening ports (TCP/UDP) using networking utilities (`netstat`, `ss`, or `lsof`).
- Save the active connections report to `/home/ubuntu/listening_ports.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 0 Marks |
| **TC2**   | File `/home/ubuntu/etc_size.txt` contains `/etc/` disk size details | 3 Marks |
| **TC3**   | File `/home/ubuntu/local_ips.txt` created successfully | 3 Marks |
| **TC4**   | File `local_ips.txt` lists config files referencing `127.0.0.1` | 3 Marks |
| **TC5**   | File `/home/ubuntu/listening_ports.txt` created successfully | 3 Marks |
| **TC6**   | Listening ports file contains active TCP/UDP socket endpoints | 4 Marks |
| **TC7**   | Diagnostic logs timestamped and verified for active session | 4 Marks |

**Total Score: 20 Marks**
