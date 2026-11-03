# Windows Server Basics: Navigation, Environment Variables & file manipulation

**Difficulty Level:** Medium

**Duration:** 60 Minutes

## Scenario

As a Windows System Administrator, you are tasked with setting up a baseline environment on a newly provisioned Windows Server. You need to establish a workspace folder layout, configure system-wide environment variables, capture basic server metadata, and locate system log files.

## Task Objectives

Perform the following actions on this local Windows Virtual Machine:

### 1. Local Environment Verification

- **Workspace Path:** Ensure you are working directly on this local Windows Virtual Machine.
- **Goal:** Your session starts when you access this machine. Ensure you are ready to begin file and system manipulations natively.

### 2. Configure Directory Layout

On the running Windows Server instance, create the following directory structure:

- `C:\workspace\logs`
- `C:\workspace\backups`

### 3. Set Up System Environment Variables

Configure a system-wide environment variable named `APP_ENVIRONMENT` and assign it the value `production`.

- The variable must be set at the **System (Machine)** level so that it persists across reboots and is accessible by all user accounts.

### 4. System Metadata and Log Auditing

- Retrieve the computer hostname and operating system details, and write this information to `C:\workspace\sysinfo.txt`.
- Locate all log files ending in `.log` within the `C:\Windows` directory (non-recursively, just inside the root `C:\Windows` folder) and write their absolute paths (one path per line) to `C:\workspace\log_files.txt`.

Once you have performed the tasks, you can run the verification script. The verification script will evaluate the configuration of your local Windows VM by verifying directory pathways, environment variables, and file content directly.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                              | Validation                                                                           | Marks   |
| ------------- | ---------------------------------------- | ------------------------------------------------------------------------------------ | ------- |
| **TC1** | **Local Environment Verification** | Validation of standard local execution environment and session active status.        | 0 Marks |
| **TC2** | **Logs Directory Structure**       | Folder`C:\workspace\logs` exists on the machine.                                   | 4 Marks |
| **TC3** | **Backups Directory Structure**    | Folder`C:\workspace\backups` exists on the machine.                                | 4 Marks |
| **TC4** | **System Environment Variables**   | System environment variable`APP_ENVIRONMENT` is set permanently to `production`. | 4 Marks |
| **TC5** | **System Metadata**                | File`sysinfo.txt` exists in `C:\workspace` with correct contents.                | 4 Marks |
| **TC6** | **Log Auditing**                   | File`log_files.txt` exists in `C:\workspace` with correct contents.              | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Make sure to set the environment variable at the Machine level (e.g. using `[Environment]::SetEnvironmentVariable("APP_ENVIRONMENT", "production", "Machine")` or Windows GUI).
- File paths inside `log_files.txt` must be absolute paths (e.g., `C:\Windows\setupact.log`) separated by newlines.
