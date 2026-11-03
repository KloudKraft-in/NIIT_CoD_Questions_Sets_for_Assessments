# Storage Lab: Linux Application Volume Capacity Triage & Large File Discovery

Duration : 30 Min.

## Scenario
An enterprise application server's dedicated data volume `/data` (or `/opt/app_data`) has reached 96% utilization with only 4% free space remaining. The administrator cannot delete files at random because mission-critical services depend on the volume. The engineer must log in via SSH to the Linux system, inspect filesystem mount states, execute a recursive search and sorting pipeline to identify the largest files (orphaned database dumps, stale staging tarballs, runaway debug logs), sort them in descending order of size, and generate a structured cleanup candidate report `large_files_report.json`.

## Task Objectives
Perform the following storage capacity triage tasks inside your `student_workspace` directory:

> **Pre-Staged Files in `student_workspace/`:**
> - **`mock_data_volume/`**: Simulated application storage hierarchy containing candidate files.
> - **`large_files_report.json`**: Pre-staged JSON boilerplate file with standard keys (`file_path`, `size_mb`, `last_modified`).

### 1. Filesystem Capacity Inspection
- Inspect filesystem disk space usage to isolate mounted partitions and identify critical capacity exhaustion.

### 2. Recursive Search & Sorting Pipeline
- Recursively scan `mock_data_volume/` to discover all large candidate files and rank them in descending order by size.

### 3. Candidate Report Generation
- Directly edit `large_files_report.json` in your workspace and replace the `TODO_*` placeholders with the top identified file paths, formatted sizes in MB (or GB), and modification timestamps.

## Verification
Once you have populated `large_files_report.json`, test your solution locally by running:
```bash
python run.py
```
Once verified, click **"Run Tests"** on the assessment platform to record your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Volume query: accurate Linux filesystem inspection via df -hT isolating capacity bottlenecks | 4 Marks |
| **TC2** | Recursive search & sorting: find command pipeline correctly identifies and sorts large files | 3 Marks |
| **TC3** | JSON report formatting: large_files_report.json contains valid paths, formatted sizes, and timestamps | 3 Marks |

**Total Score: 10 Marks**

## Cross-Platform Reference Note
In enterprise operations, Linux administrators execute recursive find/sort pipelines on storage mount points, whereas Windows administrators execute PowerShell cmdlets (`Get-Volume` and `Get-ChildItem`). Both SOPs fulfill the core change-controlled space recovery workflow.
