# Linux Lab: Linux Network Troubleshooting & Archiving (Local VM)

Duration : 60 Min.

## Scenario

As part of a routine system audit, you must verify the external network connectivity of your local Ubuntu VM, retrieve network IP configuration, identify which TCP/UDP ports are actively listening on the host, and securely archive a set of dummy log files for backup using tarball compression.

## Task Objectives

Perform the following actions inside the default home directory (`/home/<username>`) of the local Ubuntu system:

### 1. Environment Verification

- Ensure the local VM environment is running with your default home directory (`/home/<username>`).

### 2. Network Connectivity & Port Diagnostics

- Test external network connectivity by sending exactly 4 ICMP ping packets to `google.com` and save the entire output to `/home/<username>/ping_results.txt`.
- Identify all actively listening TCP and UDP network ports on the instance (using `ss -tuln` or `netstat -tuln`) and save the output to `/home/<username>/open_ports.txt`.
- Retrieve the system's IP address configuration (using `ip a` or `ifconfig`) and save the output to `/home/<username>/ip_config.txt`.

### 3. File Creation & Archiving

- Create a dummy log file named `dummy_app.log` in `/home/<username>`.
- Compress this file into a gzip tarball archive named `app_archive.tar.gz` located in `/home/<username>`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                                       | Marks   |
| ------------- | --------------------------------------------------------------------------------- | ------- |
| **TC1** | Local VM Environment active and verified                                          | 0 Marks |
| **TC2** | Network Connectivity verified (`ping_results.txt` indicates successful packets) | 4 Marks |
| **TC3** | Port diagnostics (`open_ports.txt` generated correctly)                         | 4 Marks |
| **TC4** | System IP configuration retrieved (`ip_config.txt` generated)                   | 4 Marks |
| **TC5** | Dummy log file (`dummy_app.log`) created successfully                           | 4 Marks |
| **TC6** | Compression (`app_archive.tar.gz` exists and contains `dummy_app.log`)        | 4 Marks |

**Total Score: 20 Marks**
