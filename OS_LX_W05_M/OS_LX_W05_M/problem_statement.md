# Linux Lab: systemd Service Unit Management, Dependency Mapping & Failure Recovery (Local VM)

Duration : 60 Min.

## Scenario

A critical backend microservice (orders-api.service) fails to start after an operating system reboot. The service unit enters an 'activating (auto-restart)' loop. You must inspect journalctl error messages, trace the systemd dependency tree to find a blocked prerequisite service, resolve the dependency failure, and verify clean startup and boot enablement.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Interrogate the failing service

- Interrogate the failing service using systemctl status orders-api and journalctl -u orders-api -xe.

### 2. Map the service dependency

- Map the service dependency tree using systemctl list-dependencies orders-api to isolate the failed required unit.

### 3. Correct the underlying unit

- Correct the underlying unit failure (missing socket directory or permission fault), start the prerequisite service, and restart orders-api.

### 4. Enable orders-api to ensure

- Enable orders-api to ensure persistent auto-start on system boot.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Log diagnosis: journalctl logs parsed and root cause error message identified into ~/service_error.txt | 5 Marks |
| **TC2** | Dependency isolation: failed dependency unit identified via systemctl list-dependencies | 5 Marks |
| **TC3** | Service recovery: prerequisite unit and orders-api restored to active (running) state | 5 Marks |
| **TC4** | Boot persistence: systemctl is-enabled orders-api returns 'enabled' | 5 Marks |

**Total Score: 20 Marks**
