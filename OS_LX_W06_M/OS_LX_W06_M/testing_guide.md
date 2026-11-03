# Testing Guide: OS_LX_W06_M (Logrotate Configuration & Automated Log Lifecycle Management)

This comprehensive guide explains how each test case is evaluated, provides exact commands to achieve a full score (20/20), and demonstrates how each test case passes independently and fails when its respective component is removed.

---

## Grading Criteria Breakdown

| Test Case | Objective | Marks | Criteria |
| :--- | :--- | :--- | :--- |
| **TC1** | Configuration Authoring | 5 Marks | `/etc/logrotate.d/ecommerce` contains directives (`daily`, `rotate 7`, `compress`, `copytruncate`) |
| **TC2** | Syntax & Dry-Run Validation | 5 Marks | `logrotate -d /etc/logrotate.d/ecommerce` validates with zero syntax errors |
| **TC3** | Compressed Archive Generation | 5 Marks | `/var/log/ecommerce/app.log.1.gz` exists in gzip format |
| **TC4** | Copytruncate Active Handle | 5 Marks | Active log file `/var/log/ecommerce/app.log` remains intact |
| **Total** | | **20 Marks** | |

---

## Step-by-Step Implementation Guide (To score 20/20)

### Step 1: Create Log Directory and Populate Sample Active Logs (Satisfies TC4)
> **Note**: Log files must contain initial content. If the file is 0 bytes, logrotate with `notifempty` will skip rotation!

```bash
sudo mkdir -p /var/log/ecommerce
echo "Order transaction initiated: order_id=1001 user=guest" | sudo tee /var/log/ecommerce/app.log
echo "Payment gateway heartbeat OK" | sudo tee /var/log/ecommerce/error.log
sudo chmod 755 /var/log/ecommerce
sudo chmod 644 /var/log/ecommerce/*.log
```

---

### Step 2: Author the Logrotate Policy File (Satisfies TC1)
Create `/etc/logrotate.d/ecommerce` with all required directives:

```bash
sudo tee /etc/logrotate.d/ecommerce << 'EOF'
/var/log/ecommerce/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    copytruncate
}
EOF
```

---

### Step 3: Validate Syntax with Dry-Run (Satisfies TC2)
Test the configuration file using debug/dry-run mode:

```bash
sudo logrotate -d /etc/logrotate.d/ecommerce
```
*Expected Output*: Displays rotation plan without errors.

---

### Step 4: Execute Forced Rotation (Satisfies TC3 & TC4)
Trigger an immediate rotation test:

```bash
sudo logrotate -vf /etc/logrotate.d/ecommerce
```

Inspect the directory contents:
```bash
ls -la /var/log/ecommerce/
```

*Expected Result*:
- `app.log.1.gz` (Rotated and compressed archive — **TC3 passed**)
- `error.log.1.gz` (Rotated and compressed archive)
- `app.log` (Active file truncated to 0 bytes, ready for new writes — **TC4 passed**)
- `error.log` (Active file truncated to 0 bytes)

---

### Step 5: Run Verification
In the workspace, execute:
```bash
python3 student_workspace/run.py
```
Or click **Run Tests** / **Full Eval** in the NIIT AI IDE.

**Expected Result**:
```text
TC1: Configuration authoring: /etc/logrotate.d/ecommerce contains valid directives [PASSED] (5/5)
TC2: Syntax and test execution: logrotate -d dry-run and logrotate -vf forced test complete [PASSED] (5/5)
TC3: Archive generation: rotated log file is compressed with gzip format (.1.gz) [PASSED] (5/5)
TC4: Copytruncate integrity: active log file handle remains intact with truncated zero/initial byte state [PASSED] (5/5)
TOTAL SCORE: 20/20
```

---

## Independent Pass & Fail Verification Guide

Each test case is completely decoupled. You can verify that removing any component causes ONLY that test case to fail:

### 1. Test TC1 Failure (Remove Configuration)
```bash
# Temporarily rename/remove the configuration file
sudo mv /etc/logrotate.d/ecommerce /etc/logrotate.d/ecommerce.bak

# Run tests:
# -> TC1: FAILED (0/5)
# -> TC2: FAILED (0/5) (Config missing)
# -> TC3: PASSED (5/5) (Archive still exists)
# -> TC4: PASSED (5/5) (Active log still exists)
# Score: 10/20

# Restore:
sudo mv /etc/logrotate.d/ecommerce.bak /etc/logrotate.d/ecommerce
```

---

### 2. Test TC2 Failure (Introduce Syntax Error)
```bash
# Append an invalid directive to the config
echo "unsupported_directive_syntax_error" | sudo tee -a /etc/logrotate.d/ecommerce

# Run tests:
# -> TC1: PASSED (5/5) (Directives present)
# -> TC2: FAILED (0/5) (Syntax error detected by logrotate -d)
# -> TC3: PASSED (5/5)
# -> TC4: PASSED (5/5)
# Score: 15/20

# Restore by removing the invalid line:
sudo sed -i '/unsupported_directive_syntax_error/d' /etc/logrotate.d/ecommerce
```

---

### 3. Test TC3 Failure (Remove Rotated Archive)
```bash
# Remove only the compressed archive
sudo rm -f /var/log/ecommerce/*.gz

# Run tests:
# -> TC1: PASSED (5/5)
# -> TC2: PASSED (5/5)
# -> TC3: FAILED (0/5) (Archive .1.gz not found)
# -> TC4: PASSED (5/5) (Active log file still exists)
# Score: 15/20

# Restore:
echo "New traffic log data" | sudo tee -a /var/log/ecommerce/app.log
sudo logrotate -vf /etc/logrotate.d/ecommerce
```

---

### 4. Test TC4 Failure (Remove Active Log File)
```bash
# Remove active log file
sudo rm -f /var/log/ecommerce/app.log /var/log/ecommerce/error.log

# Run tests:
# -> TC1: PASSED (5/5)
# -> TC2: PASSED (5/5)
# -> TC3: PASSED (5/5) (Archive .1.gz still present)
# -> TC4: FAILED (0/5) (Active log missing)
# Score: 15/20

# Restore:
echo "Active logging resumed" | sudo tee /var/log/ecommerce/app.log
```
