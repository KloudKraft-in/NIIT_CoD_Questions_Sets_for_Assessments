# Linux Lab: File Content Search & Text Filtering via Pipeline Commands (Local VM)

Duration : 30 Min.

## Scenario

An application deployment has generated scattered log files and configuration fragments. You must use utility commands to locate specific configuration files, filter error messages, sort occurrences, and generate a consolidated report.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Search for all files

- Search for all files ending with .conf under /opt/app_data/ and save their file paths to ~/found_configs.txt.

### 2. Parse the provided sample

- Parse the provided sample application log /opt/app_data/server.log for lines matching 'CRITICAL' (case-insensitive).

### 3. Sort the matching lines

- Sort the matching lines alphabetically, count the unique critical errors, and write the count and sorted output to ~/critical_summary.txt.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Search execution: verify recursive search finds all .conf files and populates found_configs.txt | 4 Marks |
| **TC2** | Text filtering: case-insensitive grep correctly captures all CRITICAL lines without false positives | 3 Marks |
| **TC3** | Piping and sorting: critical_summary.txt contains correct alphabetical ordering and unique line count | 3 Marks |

**Total Score: 10 Marks**
