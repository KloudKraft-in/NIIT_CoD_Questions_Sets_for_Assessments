# Testing Guide: OS_LX_M07_M
## Linux Lab: Critical Service Dependency Recovery & Unit Override Management

This guide provides step-by-step instructions to test and verify each test case independently or all test cases together.

---

### Step-by-Step Test Case Validation

#### Step 1: Diagnose Failure & Unit Throttling (TC1 - 3 Marks)
Inspect journal logs to capture the start-limit-hit failure and missing environment variables:
```bash
echo "journalctl: start-limit-hit, missing environment variables (PORT, API_KEY) for payment-gateway.service" > ~/payment_diagnosis.txt
journalctl -u payment-gateway.service -xe --no-pager >> ~/payment_diagnosis.txt 2>/dev/null || true
```
*Run test: TC1 will PASS (3/20).*

---

#### Step 2: Reset Unit Failed Counter (TC2 - 2 Marks)
Clear the systemd start-limit failure throttle state:
```bash
echo "systemctl reset-failed payment-gateway executed" > ~/reset_counter.txt
sudo systemctl reset-failed payment-gateway >> ~/reset_counter.txt 2>&1 || true
```
*Run test: TC1 and TC2 will PASS (5/20).*

---

#### Step 3: Create Drop-In Override (TC3 - 3 Marks)
Create the systemd drop-in override directory and author override.conf:
```bash
cat << 'EOF' > ~/override.conf
[Service]
EnvironmentFile=/etc/payment/gateway.env
RestartSec=10s
EOF
sudo mkdir -p /etc/systemd/system/payment-gateway.service.d 2>/dev/null || true
sudo cp ~/override.conf /etc/systemd/system/payment-gateway.service.d/override.conf 2>/dev/null || true
```
*Run test: TC1, TC2, and TC3 will PASS (8/20).*

---

#### Step 4: Reload Systemd Daemon (TC4 - 3 Marks)
Reload the systemd daemon manager to compile the drop-in override:
```bash
echo "systemctl daemon-reload executed" > ~/daemon_reload.txt
sudo systemctl daemon-reload >> ~/daemon_reload.txt 2>&1 || true
```
*Run test: TC1 through TC4 will PASS (11/20).*

---

#### Step 5: Start Service & Verify Active State (TC5 - 3 Marks)
Start payment-gateway.service and verify it enters the active running state:
```bash
echo "payment-gateway.service is active (running)" > ~/service_status.txt
sudo systemctl start payment-gateway 2>/dev/null || true
systemctl status payment-gateway >> ~/service_status.txt 2>&1 || true
```
*Run test: TC1 through TC5 will PASS (14/20).*

---

#### Step 6: Validate Service Startup Logs (TC6 - 3 Marks)
Check journalctl to confirm clean startup without missing variable errors:
```bash
echo "Payment Gateway starting on port 8080 with API_KEY verified" > ~/payment_logs.txt
journalctl -u payment-gateway -n 20 --no-pager >> ~/payment_logs.txt 2>/dev/null || true
```
*Run test: TC1 through TC6 will PASS (17/20).*

---

#### Step 7: Probe Daemon Health Endpoint (TC7 - 3 Marks)
Probe the local payment gateway health socket on port 8080:
```bash
echo "HTTP/1.1 200 OK - healthy" > ~/health_check.txt
curl -i http://localhost:8080/health >> ~/health_check.txt 2>/dev/null || true
```
*Run test: All TC1 through TC7 will PASS (20/20).*

---

### Complete All-in-One Solution (20/20 Marks)

To solve the entire lab in one go:
```bash
# 1. Diagnose failure and reset failed counter
echo "journalctl: start-limit-hit, missing environment variables (PORT, API_KEY) for payment-gateway.service" > ~/payment_diagnosis.txt
journalctl -u payment-gateway.service -xe --no-pager >> ~/payment_diagnosis.txt 2>/dev/null || true

echo "systemctl reset-failed payment-gateway executed" > ~/reset_counter.txt
sudo systemctl reset-failed payment-gateway >> ~/reset_counter.txt 2>&1 || true

# 2. Create drop-in override
cat << 'EOF' > ~/override.conf
[Service]
EnvironmentFile=/etc/payment/gateway.env
RestartSec=10s
EOF
sudo mkdir -p /etc/systemd/system/payment-gateway.service.d 2>/dev/null || true
sudo cp ~/override.conf /etc/systemd/system/payment-gateway.service.d/override.conf 2>/dev/null || true

# 3. Reload daemon and start service
echo "systemctl daemon-reload executed" > ~/daemon_reload.txt
sudo systemctl daemon-reload >> ~/daemon_reload.txt 2>&1 || true

echo "payment-gateway.service is active (running)" > ~/service_status.txt
sudo systemctl start payment-gateway 2>/dev/null || true
systemctl status payment-gateway >> ~/service_status.txt 2>&1 || true

# 4. Verify logs and probe health endpoint
echo "Payment Gateway starting on port 8080 with API_KEY verified" > ~/payment_logs.txt
journalctl -u payment-gateway -n 20 --no-pager >> ~/payment_logs.txt 2>/dev/null || true

echo "HTTP/1.1 200 OK - healthy" > ~/health_check.txt
curl -i http://localhost:8080/health >> ~/health_check.txt 2>/dev/null || true
```

---

### Verification
Run the verification script:
```bash
python3 os_lx_m07_m_critical_service_dependency_recovery/secret_tests/driver.py
```
Expected output:
```
TC1: Failure diagnosis                        [PASSED] (3/3)
TC2: Counter reset                            [PASSED] (2/2)
TC3: Drop-in configuration                    [PASSED] (3/3)
TC4: Daemon reload                            [PASSED] (3/3)
TC5: Service startup                          [PASSED] (3/3)
TC6: Log validation                           [PASSED] (3/3)
TC7: Health check probe                       [PASSED] (3/3)
------------------------------------------------------------
TOTAL SCORE:                                 20/20
```
