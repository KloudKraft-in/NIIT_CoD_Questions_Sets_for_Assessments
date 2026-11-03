# Linux Lab: System Log Reading & Spike Window Isolation (Local VM)

Duration : 30 Min.

## Scenario

An intermittent service degradation occurred between 14:00:00 and 14:15:00 UTC. As an L2 Linux support analyst, you must interrogate /var/log/syslog, count error occurrences, isolate entries within the specific time window, and extract the offending client IP addresses.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Count total occurrences of

- Count total occurrences of 'ERROR' and 'TIMEOUT' in /var/log/syslog and write counts to ~/log_metrics.txt.

### 2. Filter all log entries

- Filter all log entries between '14:00:00' and '14:15:00' into ~/incident_window.log.

### 3. Extract all unique IP

- Extract all unique IP addresses associated with error lines in the incident window and save to ~/culprit_ips.txt.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Log metrics accuracy: total count of ERROR and TIMEOUT correctly calculated | 3 Marks |
| **TC2** | Timestamp window isolation: incident_window.log contains strictly entries within 14:00:00-14:15:00 | 3 Marks |
| **TC3** | Regex IP extraction: culprit_ips.txt contains valid IPv4 addresses extracted from log lines | 2 Marks |
| **TC4** | Deduplication: culprit_ips.txt contains uniquely sorted IP entries with no duplicates | 2 Marks |

**Total Score: 10 Marks**
