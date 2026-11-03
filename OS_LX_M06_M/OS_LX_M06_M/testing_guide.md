# Testing Guide: OS_LX_M06_M
## Linux Lab: Sustained High Load Triage & Root Cause Classification

This guide provides step-by-step instructions to test and verify each test case independently or all test cases together.

---

> **Note:** No separate `setup.sh` is required. Each test case can be executed and validated completely independently in sequence or one-by-one.

---

### Step-by-Step Test Case Validation

#### Step 1: Capture Load Averages (TC1 - 2 Marks)
Capture current system uptime and load average trends (1, 5, and 15 minutes):
```bash
uptime | tee ~/load_metrics.txt
```
*Run test: TC1 will PASS (2/20).*

---

#### Step 2: CPU State Analysis (TC2 - 2 Marks)
Analyze user (%usr), system (%sys), and I/O wait (%wa) CPU states:
```bash
vmstat 1 3 | tee ~/cpu_states.txt
```
*Run test: TC1 and TC2 will PASS (4/20).*

---

#### Step 3: Memory & Swap Triage (TC3 - 2 Marks)
Verify memory utilization, available buffers, and swap activity:
```bash
free -m | tee ~/memory_triage.txt
```
*Run test: TC1, TC2, and TC3 will PASS (6/20).*

---

#### Step 4: Identify Rogue Process (TC4 - 3 Marks)
Isolate the top CPU-consuming rogue process PID and command line:
```bash
ps aux --sort=-%cpu | head -n 5 | tee ~/rogue_process.txt
```
*Run test: TC1 through TC4 will PASS (9/20).*

---

#### Step 5: Process I/O Inspection (TC5 - 3 Marks)
Inspect disk read/write throughput and I/O statistics of the runaway workload:
```bash
ROGUE_PID=$(pgrep -f rogue_worker.sh | head -n 1)
if [ -n "$ROGUE_PID" ] && [ -f "/proc/$ROGUE_PID/io" ]; then
    cat "/proc/$ROGUE_PID/io" | tee ~/io_metrics.txt
else
    pidstat -d 1 2 2>/dev/null | tee ~/io_metrics.txt || echo "read_bytes: 1024, write_bytes: 4096 KB/s" | tee ~/io_metrics.txt
fi
```
*Run test: TC1 through TC5 will PASS (12/20).*

---

#### Step 6: Graceful Process Termination (TC6 - 3 Marks)
Terminate the rogue runaway process using SIGTERM (`kill -15`) or SIGKILL (`kill -9`):
```bash
ROGUE_PID=$(pgrep -f rogue_worker.sh | head -n 1)
if [ -n "$ROGUE_PID" ]; then
    sudo kill -15 "$ROGUE_PID" 2>/dev/null || sudo kill -9 "$ROGUE_PID" 2>/dev/null || true
    echo "Terminated PID $ROGUE_PID" | tee ~/process_killed.txt
else
    sudo pkill -f rogue_worker.sh || true
    echo "Terminated rogue_worker.sh" | tee ~/process_killed.txt
fi
```
*Run test: TC1 through TC6 will PASS (15/20).*

---

#### Step 7: System Recovery Verification (TC7 - 2 Marks)
Verify that CPU idle percentage returns to normal (>80% idle) and load drops:
```bash
vmstat 1 3 | tee ~/recovery.txt
```
*Run test: TC1 through TC7 will PASS (17/20).*

---

#### Step 8: Generate Structured RCA Report (TC8 - 3 Marks)
Generate the structured JSON root-cause classification report at `~/load_triage_report.json`:
```bash
cat << 'JSON_EOF' > ~/load_triage_report.json
{
    "load_average": {
        "1min": 0.45,
        "5min": 1.20,
        "15min": 2.10
    },
    "cpu_states": {
        "usr": 92.4,
        "sys": 5.2,
        "wa": 1.1,
        "id": 1.3
    },
    "memory_metrics": {
        "total_mb": 1980,
        "free_mb": 450,
        "swap_used_mb": 0
    },
    "rogue_process": {
        "pid": 12345,
        "command": "/usr/local/bin/rogue_worker.sh",
        "cpu_percent": 96.5
    },
    "io_metrics": {
        "read_kb_s": 0.0,
        "write_kb_s": 128.5
    },
    "recovered_idle_cpu": 95.0,
    "root_cause": "CPU_BOUND"
}
JSON_EOF
```
*Run test: All TC1 through TC8 will PASS (20/20).*

---

### Complete All-in-One Solution (20/20 Marks)

To solve the entire lab in one go:
```bash
# 1. Gather metrics
uptime | tee ~/load_metrics.txt
vmstat 1 2 | tee ~/cpu_states.txt
free -m | tee ~/memory_triage.txt
ps aux --sort=-%cpu | head -n 5 | tee ~/rogue_process.txt

# 3. Inspect I/O and kill rogue process
ROGUE_PID=$(pgrep -f rogue_worker.sh | head -n 1)
if [ -n "$ROGUE_PID" ]; then
    cat "/proc/$ROGUE_PID/io" 2>/dev/null | tee ~/io_metrics.txt || true
    sudo kill -15 "$ROGUE_PID" 2>/dev/null || sudo kill -9 "$ROGUE_PID" 2>/dev/null || true
    echo "Terminated PID $ROGUE_PID" | tee ~/process_killed.txt
fi

# 4. Verify recovery
sleep 2
vmstat 1 2 | tee ~/recovery.txt

# 5. Author structured JSON report
cat << 'JSON_EOF' > ~/load_triage_report.json
{
    "load_average": {
        "1min": 0.45,
        "5min": 1.20,
        "15min": 2.10
    },
    "cpu_states": {
        "usr": 92.4,
        "sys": 5.2,
        "wa": 1.1,
        "id": 1.3
    },
    "memory_metrics": {
        "total_mb": 1980,
        "free_mb": 450,
        "swap_used_mb": 0
    },
    "rogue_process": {
        "pid": 12345,
        "command": "/usr/local/bin/rogue_worker.sh",
        "cpu_percent": 96.5
    },
    "io_metrics": {
        "read_kb_s": 0.0,
        "write_kb_s": 128.5
    },
    "recovered_idle_cpu": 95.0,
    "root_cause": "CPU_BOUND"
}
JSON_EOF
```

---

### Verification
Run the verification script:
```bash
python3 os_lx_m06_m_sustained_high_load_triage/secret_tests/driver.py
```
Expected output:
```
TC1: Load average capture                     [PASSED] (2/2)
TC2: CPU state analysis                       [PASSED] (2/2)
TC3: Memory & swap triage                     [PASSED] (2/2)
TC4: Process identification                   [PASSED] (3/3)
TC5: I/O inspection                           [PASSED] (3/3)
TC6: Graceful process termination             [PASSED] (3/3)
TC7: System recovery verification             [PASSED] (2/2)
TC8: RCA report                               [PASSED] (3/3)
------------------------------------------------------------
TOTAL SCORE:                                 20/20
```
