# Linux Lab: Performance Metric Baseline Sweep & System Health Scripting (Local VM)

Duration : 30 Min.

## Scenario

Operations leadership requires a standardized automated bash script that executes during morning shift changes across all Linux hosts to generate a structured system health baseline.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Author an executable bash

- Author an executable bash script named ~/scripts/health_sweep.sh.

### 2. The script must capture

- The script must capture: system uptime/load average, total vs free memory, root filesystem percentage used, and top 3 CPU processes.

### 3. Output the metrics in

- Output the metrics in a clean key-value format written to /var/log/daily_health_sweep.log.

### 4. Ensure the script handles

- Ensure the script handles non-root execution gracefully with proper exit codes.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Script executable permissions: ~/scripts/health_sweep.sh has +x execution rights and valid shebang | 2 Marks |
| **TC2** | Load and memory parsing: uptime load average and free memory parsed and formatted cleanly | 3 Marks |
| **TC3** | Filesystem and process metrics: root disk utilization percentage and top 3 CPU processes captured | 3 Marks |
| **TC4** | Log destination and exit code: output written to /var/log/daily_health_sweep.log and script exits with code 0 | 2 Marks |

**Total Score: 10 Marks**
