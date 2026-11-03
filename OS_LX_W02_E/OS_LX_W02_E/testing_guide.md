# Testing Guide: OS_LX_W02_E (System Log Reading & Spike Window Isolation)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

---

## Step 1: Initialize /var/log/syslog (If Missing or Empty)

Modern Ubuntu distributions (such as Ubuntu 24.04 LTS and minimal cloud/container environments) do not run `rsyslog` by default, so `/var/log/syslog` may not exist on your VM.

To initialize `/var/log/syslog` with the lab's simulated incident logs, run:

```bash
# Option A: Run the setup script
sudo bash setup.sh

# Option B: Or paste this one-liner in terminal:
sudo mkdir -p /var/log && sudo tee /var/log/syslog << 'EOF'
Oct 27 13:45:10 web-srv01 systemd[1]: Started Daily apt upgrade and clean activities.
Oct 27 13:58:20 web-srv01 app[1042]: INFO Health check responding OK on port 8080
Oct 27 14:02:15 web-srv01 app[1042]: ERROR Database connection failure from 192.168.1.105
Oct 27 14:05:32 web-srv01 app[1042]: TIMEOUT Upstream gateway response timeout for client 10.0.0.45
Oct 27 14:08:19 web-srv01 app[1042]: ERROR Failed to authenticate user session from 172.16.0.88
Oct 27 14:12:44 web-srv01 app[1042]: TIMEOUT Request timeout from 192.168.1.105
Oct 27 14:14:50 web-srv01 app[1042]: ERROR Critical thread pool exhaustion caused by 10.0.0.45
Oct 27 14:18:05 web-srv01 app[1042]: INFO Service stabilized, normal latency restored
Oct 27 14:25:30 web-srv01 systemd[1]: Session 3 logged out.
EOF
sudo chmod 644 /var/log/syslog
```

---

## Step 2: Execute Linux Commands for Assessment Objectives

Switch to the user directory (`cd ~`) and execute the following commands:

### Task 1: Count total occurrences of 'ERROR' and 'TIMEOUT'
Count the occurrences in `/var/log/syslog` and write the counts to `~/log_metrics.txt`:

```bash
echo "ERROR: $(grep -c 'ERROR' /var/log/syslog)" > ~/log_metrics.txt
echo "TIMEOUT: $(grep -c 'TIMEOUT' /var/log/syslog)" >> ~/log_metrics.txt
```

### Task 2: Filter all log entries between '14:00:00' and '14:15:00'
Extract log lines matching the incident time window into `~/incident_window.log`:

```bash
grep -E "14:(0[0-9]|1[0-5]):[0-9]{2}" /var/log/syslog > ~/incident_window.log
```

### Task 3 & 4: Extract all unique IP addresses from incident errors
Extract unique IPv4 addresses from the error/timeout lines in `~/incident_window.log` and save to `~/culprit_ips.txt`:

```bash
grep -E "(ERROR|TIMEOUT)" ~/incident_window.log | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" | sort -u > ~/culprit_ips.txt
```

---

## Step 3: Verification

To verify your solution, execute the verification script:

```bash
python3 student_workspace/run.py
```

Expected Output:
```text
TC1: Log metrics accuracy: total count of ERROR and TIMEOUT correctly calculated [PASSED] (3/3)
TC2: Timestamp window isolation: incident_window.log contains strictly entries within 14:00:00-14:15:00 [PASSED] (3/3)
TC3: Regex IP extraction: culprit_ips.txt contains valid IPv4 addresses extracted from log lines [PASSED] (2/2)
TC4: Deduplication: culprit_ips.txt contains uniquely sorted IP entries with no duplicates [PASSED] (2/2)
------------------------------------------------------------
TOTAL SCORE:                                 10/10
```
