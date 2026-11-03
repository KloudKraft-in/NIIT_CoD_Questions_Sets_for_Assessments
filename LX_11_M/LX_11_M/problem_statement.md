# Linux Lab: Memory Log Rotation and Cron Telemetry (Local VM)

Duration : 60 Min.

## Scenario

As a System Reliability Engineer, you are asked to build an automated telemetry and diagnostic monitoring setup on an Ubuntu Linux server. This involves auditing memory allocation trends, searching system logs for failure events, and configuring regular cron automated reporting.

## Task Objectives

Perform the following actions on your local Linux system:

### 1. Environment Verification
- Ensure the local VM environment is active under your default home directory (`/home/ubuntu`).

### 2. Telemetry Workspace Setup
- Create a directory named `/home/ubuntu/telemetry/`.

### 3. Memory Process Audit
- Capture the **top 3 memory-consuming processes** using `ps` (sorted by RSS/memory usage).
- Write their details (`PID`, `%MEM`, and `COMMAND` or equivalent full line output) to `/home/ubuntu/telemetry/memory_hogs.txt`.

### 4. Critical Event Log Search
- Search system logs (e.g. `/var/log/dpkg.log` or `/var/log/syslog`) for any line containing `"fail"` or `"critical"` (case-insensitive).
- Save the last 15 matching occurrences to `/home/ubuntu/telemetry/critical_events.log`.

### 5. Automated Cron Telemetry Setup
- Register a user cron job for the `ubuntu` user using `crontab -e`.
- Configure the cron job to run **every 5 minutes** (`*/5 * * * *`).
- The job must append the current timestamp (`date`) and CPU load statistics (e.g. `uptime`) to `/home/ubuntu/telemetry/cpu_load.log`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 0 Marks |
| **TC2**   | Telemetry directory `/home/ubuntu/telemetry/` created | 3 Marks |
| **TC3**   | File `memory_hogs.txt` contains top 3 memory-consuming processes | 3 Marks |
| **TC4**   | Process metadata formatting verified (`PID`, `%MEM`, command) | 3 Marks |
| **TC5**   | Log file `critical_events.log` contains filtered error events | 3 Marks |
| **TC6**   | User cron job registered for `ubuntu` running every 5 minutes | 4 Marks |
| **TC7**   | Cron job configured to append timestamp/CPU load to `cpu_load.log` | 4 Marks |

**Total Score: 20 Marks**
