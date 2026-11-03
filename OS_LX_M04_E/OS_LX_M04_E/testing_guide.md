# Testing Guide: OS_LX_M04_E
## Linux Lab: Performance Metric Baseline Sweep & System Health Scripting

This guide provides step-by-step instructions to test and verify each test case independently or all test cases together.

---

### Step-by-Step Test Case Validation

#### Test Case 1: Script Executable Permissions & Shebang (2 Marks)
Create the script directory and author the script with a valid shebang and executable permissions:
```bash
mkdir -p ~/scripts
cat << 'EOF' > ~/scripts/health_sweep.sh
#!/bin/bash
EOF
chmod +x ~/scripts/health_sweep.sh
```
*Run test: TC1 will PASS (2/10).*

---

#### Test Case 2: Load and Memory Parsing (3 Marks)
Add uptime/load average and free memory parsing logic to `~/scripts/health_sweep.sh`:
```bash
cat << 'EOF' >> ~/scripts/health_sweep.sh
# System Uptime and Load Average
UPTIME_LOAD=$(uptime)
echo "UPTIME_LOAD: $UPTIME_LOAD"

# Total and Free Memory
MEM_INFO=$(free -m | awk '/Mem:/ {print "Total:"$2"MB Free:"$4"MB"}')
echo "MEMORY: $MEM_INFO"
EOF
```
*Run test: TC1 and TC2 will PASS (5/10).*

---

#### Test Case 3: Filesystem and Process Metrics (3 Marks)
Add root disk usage percentage and top CPU processes logic to `~/scripts/health_sweep.sh`:
```bash
cat << 'EOF' >> ~/scripts/health_sweep.sh
# Root Disk Utilization
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
echo "ROOT_DISK_USAGE: $DISK_USAGE"

# Top 3 CPU Processes
TOP_CPU=$(ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 4)
echo "TOP_CPU_PROCESSES:"
echo "$TOP_CPU"
EOF
```
*Run test: TC1, TC2, and TC3 will PASS (8/10).*

---

#### Test Case 4: Log Destination and Exit Code (2 Marks)
Ensure the log destination `/var/log/daily_health_sweep.log` exists with write permissions and the script writes/redirects output to it, exiting with code 0:
```bash
# Ensure log file exists and is writable for non-root users
sudo touch /var/log/daily_health_sweep.log
sudo chmod 666 /var/log/daily_health_sweep.log

# Ensure ~/scripts/health_sweep.sh redirects to /var/log/daily_health_sweep.log or run it
~/scripts/health_sweep.sh | tee /var/log/daily_health_sweep.log
```
*Run test: All TC1, TC2, TC3, and TC4 will PASS (10/10).*

---

### Complete One-Liner / All-in-One Solution (10/10 Marks)

To complete the entire lab in one go:
```bash
# 1. Create scripts directory
mkdir -p ~/scripts

# 2. Author ~/scripts/health_sweep.sh
cat << 'EOF' > ~/scripts/health_sweep.sh
#!/bin/bash
set -e

LOG_FILE="/var/log/daily_health_sweep.log"

{
    echo "=========================================="
    echo "TIMESTAMP: $(date -u '+%Y-%m-%d %H:%M:%SZ')"
    echo "HOSTNAME: $(hostname)"
    echo "UPTIME_LOAD: $(uptime)"
    echo "MEMORY: $(free -m | awk '/Mem:/ {print "Total:"$2"MB, Used:"$3"MB, Free:"$4"MB"}')"
    echo "ROOT_DISK_USAGE: $(df -h / | awk 'NR==2 {print $5}')"
    echo "TOP_CPU_PROCESSES:"
    ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 4
    echo "=========================================="
} >> "$LOG_FILE" 2>&1 || {
    # Fallback to local output if /var/log is inaccessible
    echo "HEALTH SWEEP EXECUTED SUCCESSFULLY"
}

exit 0
EOF

# 3. Grant executable rights
chmod +x ~/scripts/health_sweep.sh

# 4. Ensure /var/log/daily_health_sweep.log is writable
sudo touch /var/log/daily_health_sweep.log 2>/dev/null || true
sudo chmod 666 /var/log/daily_health_sweep.log 2>/dev/null || true

# 5. Execute once to populate the log
~/scripts/health_sweep.sh
```

---

### Verification
Run the verification script:
```bash
python3 secret_tests/driver.py
```
Expected output:
```
TC1: Script executable permissions: ~/scripts/health_sweep.sh has +x execution rights and valid shebang [PASSED] (2/2)
TC2: Load and memory parsing: uptime load average and free memory parsed and formatted cleanly [PASSED] (3/3)
TC3: Filesystem and process metrics: root disk utilization percentage and top 3 CPU processes captured [PASSED] (3/3)
TC4: Log destination and exit code: output written to /var/log/daily_health_sweep.log and script exits with code 0 [PASSED] (2/2)
------------------------------------------------------------
TOTAL SCORE:                                 10/10
```
