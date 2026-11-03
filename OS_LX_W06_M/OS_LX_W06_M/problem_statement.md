# Linux Lab: Logrotate Configuration & Automated Log Lifecycle Management (Local VM)

Duration : 60 Min.

## Scenario

Application log files in /var/log/ecommerce/ are growing uncontrollably, threatening to exhaust disk space on the root partition. You must author a robust logrotate policy file that rotates logs daily, retains 7 compressed archives, implements copytruncate to prevent disrupting active file handles, and forces rotation testing.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Create directory /var/log/ecommerce/ with

- Create directory /var/log/ecommerce/ with sample active logs app.log and error.log.

### 2. Author a configuration file

- Author a configuration file /etc/logrotate.d/ecommerce with daily rotation, rotate 7, compress, missingok, notifempty, and copytruncate.

### 3. Execute a forced rotation

- Execute a forced rotation test using logrotate -vf /etc/logrotate.d/ecommerce.

### 4. Verify that app.log.1.gz is

- Verify that app.log.1.gz is created, original app.log is truncated with 0 bytes, and active processes continue logging.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Configuration authoring: /etc/logrotate.d/ecommerce contains valid directives (daily, rotate 7, compress, copytruncate) | 5 Marks |
| **TC2** | Syntax and test execution: logrotate -d dry-run and logrotate -vf forced test complete with zero syntax errors | 5 Marks |
| **TC3** | Archive generation: rotated log file is compressed with gzip format (.1.gz) | 5 Marks |
| **TC4** | Copytruncate integrity: active log file handle remains intact with truncated zero/initial byte state | 5 Marks |

**Total Score: 20 Marks**
