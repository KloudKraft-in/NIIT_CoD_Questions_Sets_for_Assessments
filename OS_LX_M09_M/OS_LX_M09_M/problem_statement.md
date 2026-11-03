# Linux Lab: Comprehensive Enterprise Linux Outage Resolution & Runbook Execution (Local VM)

Duration : 90 Min.

## Scenario

A catastrophic multi-fault incident strikes an enterprise production server following an uncoordinated patch cycle: the web server is stopped, /var is at 100% capacity due to runaway uncompressed logs, an orphaned process is deadlocking database files, and a misconfigured network route blocks remote API traffic. You must follow a disciplined runbook sequence to triage, clear storage, terminate the deadlocked process, restore the network route, restart the web service, and verify platform health.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Identify the multi-fault state

- Identify the multi-fault state across disk, process, service, and network layers.

### 2. Execute safe log cleanup

- Execute safe log cleanup on /var/log/ to reduce disk utilization below 75%.

### 3. Locate and safely kill

- Locate and safely kill the orphaned deadlock process holding locked database files.

### 4. Restore the default gateway

- Restore the default gateway route in the kernel routing table.

### 5. Restart and enable the

- Restart and enable the primary web service (nginx.service).

### 6. Verify end-to-end HTTP request

- Verify end-to-end HTTP request processing on localhost.

### 7. Audit system state using

- Audit system state using uptime, df, free, and systemctl.

### 8. Author a post-incident remediation

- Author a post-incident remediation log in /var/log/incident_recovery.log.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Initial triage assessment: multi-fault symptom log created identifying all 4 failure points | 2 Marks |
| **TC2** | Disk capacity recovery: /var partition cleaned safely without deleting active database files | 3 Marks |
| **TC3** | Orphaned process cleanup: locked process identified via fuser/lsof and terminated cleanly | 3 Marks |
| **TC4** | Routing restoration: default gateway route restored and verified via ip route | 2 Marks |
| **TC5** | Service restoration: nginx.service started and verified in active (running) state | 3 Marks |
| **TC6** | HTTP endpoint response: curl -I http://localhost/ returns HTTP 200 OK | 3 Marks |
| **TC7** | Clean system state: zero degraded systemd units and load average normal | 2 Marks |
| **TC8** | Runbook execution log: /var/log/incident_recovery.log documents timestamps and actions taken | 2 Marks |

**Total Score: 20 Marks**
