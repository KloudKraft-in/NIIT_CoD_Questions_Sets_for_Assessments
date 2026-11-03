# Linux Lab: System State & Resource Utilization Inspection (Local VM)

Duration : 30 Min.

## Scenario

Before accepting a freshly provisioned virtual machine into the production pool, an operations engineer must perform an initial health sweep. You must capture snapshot metrics of load averages, top CPU-consuming processes, memory utilization, and filesystem capacity.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Capture system load averages

- Capture system load averages using uptime and append the output to ~/system_health.txt.

### 2. Identify the top 5

- Identify the top 5 memory-consuming processes using ps aux sorted by memory and append the process list to ~/system_health.txt.

### 3. Record human-readable disk utilization

- Record human-readable disk utilization (df -hT) and memory stats in megabytes (free -m) into ~/system_health.txt.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | System load capture: uptime correctly parsed with 1/5/15 minute averages recorded | 4 Marks |
| **TC2** | Process ranking: top 5 processes by %MEM accurately captured with column headers | 3 Marks |
| **TC3** | Storage and memory metrics: df -hT filesystem table and free -m memory buffers recorded | 3 Marks |

**Total Score: 10 Marks**
