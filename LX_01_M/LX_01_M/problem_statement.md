# Linux Lab: Linux File System & Directory Navigation (Local VM)

Duration : 60 Min.

## Scenario

As a System Engineer in a technology firm, you are tasked with setting up a specific directory hierarchy for an application on a newly provisioned local Ubuntu Linux server/VM. This involves utilizing Linux directory navigation commands and file operations.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Environment Verification

- Ensure the local VM environment is running with your default home directory (`~`).

### 2. Directory Hierarchy Creation

- Create a directory hierarchy inside your home directory (`~`) containing:
  - `~/app_navigation/config`
  - `~/app_navigation/logs`

### 3. Initial File Creation

- Create the following blank files inside the newly created directories:
  - `app.conf` inside `~/app_navigation/config`
  - `error.log` inside `~/app_navigation/logs`

### 4. File Copy, Rename, and Search Operations

- Perform the following file operations:
  - Copy the `app.conf` file from `~/app_navigation/config` to `~/app_navigation/` directory.
  - Rename or move the copied file `~/app_navigation/app.conf` to `~/app_navigation/app.conf.backup`.
  - Search recursively within the `~` directory for all files or lines containing the string `"app"`, and save/append the search results to `~/search_results_nav.txt`.

### 5. Disk Space Analysis

- Perform disk analysis to check current disk space utilization, and save the formatted, human-readable report to `~/disk_usage_nav.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                                                   | Marks   |
| ------------- | --------------------------------------------------------------------------------------------- | ------- |
| **TC1** | Local VM Environment active and verified                                                      | 0 Marks |
| **TC2** | Directory hierarchy (`app_navigation/config`, `app_navigation/logs`) created successfully | 4 Marks |
| **TC3** | Initial files (`app.conf` in config, `error.log` in logs) created successfully            | 4 Marks |
| **TC4** | File operations (`cp`, `mv`/rename) performed successfully                                | 4 Marks |
| **TC5** | Keyword search results generated to`search_results_nav.txt`                                 | 4 Marks |
| **TC6** | Disk usage output (`disk_usage_nav.txt`) generated correctly                                | 4 Marks |

**Total Score: 20 Marks**
