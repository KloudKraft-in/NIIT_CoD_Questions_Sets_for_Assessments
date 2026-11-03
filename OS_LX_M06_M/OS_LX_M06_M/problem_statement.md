# Linux Lab: Sustained High Load Triage & Root Cause Classification (Local VM)

Duration : 90 Min.

## Scenario

A production server exhibits a sustained 6-hour load average climb (reaching 14.5 on a 4-core machine). As an SRE, you must execute a rigorous four-bucket diagnostic model (CPU vs Memory vs Disk I/O vs Process Starvation). You must identify the runaway process, analyze whether %wa (iowait) or %usr CPU is saturated, verify swap thrashing, terminate the offending process, and submit a root-cause classification report.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Analyze system load averages

- Analyze system load averages using uptime and vmstat 1 5.

### 2. Inspect CPU states in

- Inspect CPU states in top/htop, differentiating %usr, %sys, and %wa (iowait).

### 3. Examine memory pressure and

- Examine memory pressure and swap in/out rates using free -m and vmstat.

### 4. Identify the specific rogue

- Identify the specific rogue process PID consuming excessive cycles using ps aux --sort=-%cpu.

### 5. Check process file descriptors

- Check process file descriptors and disk I/O activity.

### 6. Terminate the rogue process

- Terminate the rogue process using kill -15 (with fallback to -9).

### 7. Verify load average drops

- Verify load average drops below warning thresholds.

### 8. Generate a structured JSON

- Generate a structured JSON root-cause report in ~/load_triage_report.json.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Load average capture: baseline load and 1/5/15 minute trends documented | 2 Marks |
| **TC2** | CPU state analysis: user vs system vs iowait (%wa) accurately differentiated | 2 Marks |
| **TC3** | Memory & swap triage: free memory and swap activity verified | 2 Marks |
| **TC4** | Process identification: rogue process PID and command line accurately isolated | 3 Marks |
| **TC5** | I/O inspection: disk write/read throughput of offending process recorded | 3 Marks |
| **TC6** | Graceful process termination: process terminated cleanly with SIGTERM/SIGKILL | 3 Marks |
| **TC7** | System recovery verification: CPU idle percentage returns to >80% | 2 Marks |
| **TC8** | RCA report: load_triage_report.json populated with valid schema and root cause call | 3 Marks |

**Total Score: 20 Marks**
