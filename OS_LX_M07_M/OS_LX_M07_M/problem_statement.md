# Linux Lab: Critical Service Dependency Recovery & Unit Override Management (Local VM)

Duration : 90 Min.

## Scenario

A payment processing daemon (payment-gateway.service) fails during startup due to missing environment variables and an overly aggressive restart policy causing systemd to throttle the unit ('start-limit-hit'). You must create a systemd drop-in override, supply the missing configuration parameters, reset the failed unit counter, and verify stable daemon execution.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Diagnose unit throttling and failure reasons

- Diagnose unit throttling and failure reasons using `systemctl status` and `journalctl -u payment-gateway.service -xe`.
- Record diagnostic failure log into `~/payment_diagnosis.txt`.

### 2. Reset systemd failed state

- Reset systemd failed state using `systemctl reset-failed payment-gateway`.
- Record the reset confirmation into `~/reset_counter.txt`.

### 3. Create a drop-in override

- Create a drop-in override configuration at `/etc/systemd/system/payment-gateway.service.d/override.conf` (or `~/override.conf`).

### 4. Configure EnvironmentFile and RestartSec

- Configure `EnvironmentFile=/etc/payment/gateway.env` and `RestartSec=10s` under `[Service]` in the override file.
- Reload the systemd manager configuration via `systemctl daemon-reload` and record to `~/daemon_reload.txt`.

### 5. Start payment-gateway.service and verify

- Start `payment-gateway.service` and verify it enters 'active (running)' state.
- Record the service status into `~/service_status.txt`.

### 6. Verify unit logs

- Verify that unit logs show successful configuration loading and service initialization.
- Record startup log verification into `~/payment_logs.txt`.

### 7. Verify health check probe

- Verify that payment gateway API responds with HTTP 200 on its local health socket (`http://localhost:8080/health`).
- Record the HTTP 200 health check response into `~/health_check.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Failure diagnosis: journalctl confirms start-limit-hit and missing environment variables | 3 Marks |
| **TC2** | Counter reset: systemctl reset-failed clears the start-limit throttle state | 2 Marks |
| **TC3** | Drop-in configuration: /etc/systemd/system/payment-gateway.service.d/override.conf created with valid syntax | 3 Marks |
| **TC4** | Daemon reload: systemctl daemon-reload executes cleanly | 3 Marks |
| **TC5** | Service startup: payment-gateway enters stable active (running) state | 3 Marks |
| **TC6** | Log validation: unit logs show successful configuration loading with zero errors | 3 Marks |
| **TC7** | Health check probe: local daemon health port responds with HTTP 200 OK | 3 Marks |

**Total Score: 20 Marks**
