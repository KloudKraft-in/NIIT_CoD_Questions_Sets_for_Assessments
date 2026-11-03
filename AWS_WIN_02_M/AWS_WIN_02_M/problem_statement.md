# Windows Server Monitoring, Logging & Service Management (file manipulation)

**Difficulty Level:** Medium

**Duration:** 60 Minutes

## Scenario

As a Windows Cloud Ops Engineer, you are responsible for maintaining server availability, configuring automated administrative scripts, monitoring CPU/memory/disk performance, validating network connectivity, and diagnosing server health issues. You need to use your local Windows Server instance to host a web service using IIS, schedule a memory monitoring task, generate disk and CPU process utilization reports, test local network connectivity, and audit critical system event errors.

## Task Objectives

Perform the following actions on your local Windows Server environment:

### 1. Local Environment Verification

- **Workspace Path:** Ensure you are working directly on this local Windows Virtual Machine.
- **Goal:** Your session starts when you access this machine. Ensure you are ready to begin system monitoring and diagnostics natively.

### 2. Install and Manage Web Services (IIS)

Install the **Web-Server (IIS)** role on the running Windows Server instance.
- Ensure that the World Wide Web Publishing Service (`W3SVC`) is enabled (configured to start automatically) and is in a `Running` state.

### 3. Configure Scheduled Memory Monitoring

Create a Windows Scheduled Task named `MemoryMonitorTask`.
- The task must run every **5 minutes** under the Local System or Administrator account.
- It must execute a command or PowerShell script that appends the current system date and free memory statistics to the log file `C:\workspace\monitor\mem_usage.log` (create the directory `C:\workspace\monitor` if it does not exist).

### 4. System Monitoring, Network Validation & Diagnostics

Ensure all reports and diagnostics logs are placed in `C:\workspace\monitor\`:
- **Disk Auditing:** Analyze disk space for the primary `C:` drive and write the disk utilization report (e.g., using `Get-PSDrive C` or `Get-Volume`) to `C:\workspace\monitor\disk_report.txt`.
- **CPU & Process Monitoring:** Identify processes consuming the most CPU by writing a report listing the top 5 CPU-consuming processes (e.g., using `Get-Process | Sort-Object CPU -Descending | Select-Object -First 5`) to `C:\workspace\monitor\cpu_process_report.txt`.
- **Network Validation & Event Logs:** Validate connectivity on the local web server port (port 80) by performing a TCP connection test (e.g. using `Test-NetConnection -Port 80`) and saving the results to `C:\workspace\monitor\network_status.txt`. Query the Windows **System Event Log** for recent events of type `Error`. Extract the description/messages of the latest 5 error entries and write them to the file `C:\workspace\monitor\event_errors.txt`.

## Verification

Once you have performed the tasks, you can run the verification script. The verification script will evaluate the configuration of your local Windows VM by verifying IIS service status, scheduled tasks, CPU/disk reports, network connection status, and event log files directly.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Validation | Marks |
| --------- | ----------- | ---------- | ----- |
| **TC1**   | **Local Environment Verification** | Validation of standard local execution environment and session active status. | 0 Marks |
| **TC2**   | **Service Management (IIS)** | Web-Server (IIS) role is installed, and the `W3SVC` service is enabled and Running. | 4 Marks |
| **TC3**   | **Automated Monitoring (Scheduled Task)** | Scheduled Task `MemoryMonitorTask` exists and is configured to log memory info. | 4 Marks |
| **TC4**   | **Disk Utilization Report** | `disk_report.txt` exists in `C:\workspace\monitor` with correct info. | 4 Marks |
| **TC5**   | **CPU Process Monitoring** | `cpu_process_report.txt` exists in `C:\workspace\monitor` with correct info. | 4 Marks |
| **TC6**   | **Network & Event Log Diagnostics** | `network_status.txt` and `event_errors.txt` exist in `C:\workspace\monitor`. | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the scheduled task name is exactly `MemoryMonitorTask`.
- Ensure all diagnostics files are written to the correct folder: `C:\workspace\monitor`.
