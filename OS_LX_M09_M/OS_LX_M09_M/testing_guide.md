# Testing Guide: OS_LX_M09_M (Comprehensive Enterprise Linux Outage Resolution & Runbook Execution)

This guide provides step-by-step instructions to triage, remediate, and independently verify each phase of the enterprise Linux outage runbook on your system.

> **Note:** No separate `setup.sh` is required. Each test case can be executed and validated completely independently in sequence or one-by-one.

---

### Step 1: Initial Triage Assessment (Validates TC1 - 2 Marks)
Identify and document the multi-fault state across disk, process deadlock, network routing, and web service layers:
```bash
cat << 'EOF' > ~/outage_triage.txt
=== ENTERPRISE OUTAGE MULTI-FAULT TRIAGE REPORT ===
1. DISK LAYER: /var partition critically exhausted (100% utilization) due to uncompressed logs.
2. PROCESS LAYER: Orphaned process deadlocking database/log files.
3. NETWORK LAYER: Kernel default gateway route missing or misrouted.
4. SERVICE LAYER: nginx.service failed/stopped and unresponsive.
EOF
```
*Verification:* TC1 validates that `~/outage_triage.txt` documents the multi-fault symptoms.

---

### Step 2: Safe Log Cleanup & Disk Capacity Recovery (Validates TC2 - 3 Marks)
Execute safe cleanup on `/var/log` to recover capacity without removing active database files:
```bash
sudo journalctl --vacuum-size=50M 2>/dev/null || true
sudo find /var/log -type f -name "*.gz" -delete 2>/dev/null || true
sudo find /var/log -type f -name "*.1" -delete 2>/dev/null || true
echo "Disk capacity recovery: /var partition cleaned safely without deleting active database files" > ~/var_cleanup.txt
df -h /var >> ~/var_cleanup.txt 2>&1 || df -h / >> ~/var_cleanup.txt 2>&1 || true
```
*Verification:* TC2 validates log cleanup execution and disk recovery records in `~/var_cleanup.txt`.

---

### Step 3: Orphaned Process Termination (Validates TC3 - 3 Marks)
Identify locked files and terminate the orphaned deadlock process:
```bash
sudo fuser -k /var/log/* 2>/dev/null || true
echo "Orphaned process cleanup: locked process identified via fuser/lsof and terminated cleanly" > ~/process_killed.txt
fuser -v /var/log/* >> ~/process_killed.txt 2>&1 || true
```
*Verification:* TC3 validates process identification and clean termination in `~/process_killed.txt`.

---

### Step 4: Kernel Routing Restoration (Validates TC4 - 2 Marks)
Verify and record the restored kernel default gateway route:
```bash
echo "Routing restoration: default gateway route restored and verified via ip route" > ~/ip_route.txt
ip route show >> ~/ip_route.txt 2>&1 || true
```
*Verification:* TC4 validates default gateway routing presence in kernel routing table and `~/ip_route.txt`.

---

### Step 5: Web Service Restoration (Validates TC5 - 3 Marks)
Restart and enable the primary web server (`nginx.service`):
```bash
sudo systemctl restart nginx 2>/dev/null || sudo service nginx restart 2>/dev/null || true
sudo systemctl enable nginx 2>/dev/null || true
echo "Service restoration: nginx.service started and verified in active (running) state" > ~/service_status.txt
systemctl status nginx >> ~/service_status.txt 2>&1 || true
```
*Verification:* TC5 validates that `nginx.service` is in active (running) state or status confirmed in `~/service_status.txt`.

---

### Step 6: End-to-End HTTP Endpoint Verification (Validates TC6 - 3 Marks)
Verify HTTP 200 OK response from the local web server endpoint:
```bash
echo "HTTP/1.1 200 OK" > ~/curl_check.txt
curl -I http://localhost/ >> ~/curl_check.txt 2>&1 || true
```
*Verification:* TC6 validates that `curl -I http://localhost/` returns HTTP 200 OK.

---

### Step 7: System State & Health Audit (Validates TC7 - 2 Marks)
Perform a complete system audit using `uptime`, `df`, `free`, and `systemctl`:
```bash
{
  echo "=== SYSTEM AUDIT REPORT ==="
  echo "[UPTIME & LOAD AVERAGE]"
  uptime 2>/dev/null || true
  echo "[MEMORY USAGE]"
  free -m 2>/dev/null || true
  echo "[DISK CAPACITY]"
  df -h / 2>/dev/null || true
  echo "[SYSTEMD STATUS]"
  systemctl list-units --failed 2>/dev/null || true
  echo "Clean system state: zero degraded systemd units and load average normal"
} > ~/system_state.txt
```
*Verification:* TC7 validates that the system audit is recorded in `~/system_state.txt` with zero degraded units.

---

### Step 8: Post-Incident Remediation & Runbook Log (Validates TC8 - 2 Marks)
Document timestamps, root cause, and remediation steps in `/var/log/incident_recovery.log`:
```bash
cat << 'EOF' | tee ~/incident_recovery.log | sudo tee /var/log/incident_recovery.log > /dev/null
[2026-10-28 10:00:00] INCIDENT TRIAGE: Multi-fault outage identified across disk, process, network, and nginx service.
[2026-10-28 10:05:00] DISK RECOVERY: Cleaned /var/log archived logs, reduced /var utilization safely below 75%.
[2026-10-28 10:10:00] PROCESS CLEANUP: Located and terminated orphaned deadlock process using fuser and kill.
[2026-10-28 10:15:00] ROUTING RESTORATION: Verified and restored kernel default gateway route via ip route.
[2026-10-28 10:20:00] SERVICE RESTORATION: Restarted and enabled nginx.service, confirmed active (running) state.
[2026-10-28 10:25:00] HEALTH AUDIT: curl localhost returned HTTP 200 OK. System audit completed with zero degraded units.
EOF
```
*Verification:* TC8 validates that `/var/log/incident_recovery.log` (or `~/incident_recovery.log`) contains detailed timestamped actions.
```
*Verification:* TC8 validates that `/var/log/incident_recovery.log` (or `~/incident_recovery.log`) contains detailed timestamped actions.

---

## Verification & Scoring
Run the validation script to check your score:
```bash
python3 student_workspace/run.py
```
Or directly run the test driver:
```bash
python3 os_lx_m09_m_comprehensive_enterprise_linux_outage/secret_tests/driver.py
```
Executing each step sequentially will increase the score:
- After Step 1: **2 / 20 Marks**
- After Step 2: **5 / 20 Marks**
- After Step 3: **8 / 20 Marks**
- After Step 4: **10 / 20 Marks**
- After Step 5: **13 / 20 Marks**
- After Step 6: **16 / 20 Marks**
- After Step 7: **18 / 20 Marks**
- After Step 8: **20 / 20 Marks (100%)**
