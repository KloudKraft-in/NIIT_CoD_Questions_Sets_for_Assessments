# Log Analysis: Automated Error Clustering & Signature Libraries

Duration : 90 Min.

## Scenario
You need to write a Python script that reads raw application logs, normalizes stack trace signatures, clusters identical errors, and matches them to runbook entries.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/cluster_errors.py`
**Input Resource File to Inspect**: `student_workspace/system_errors.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `system_errors.log` in `student_workspace/`.
- Edit `cluster_errors.py` and record the required log analytics or findings.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `system_errors.log` inside `student_workspace/`.
3. Open `cluster_errors.py` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | cluster_errors.py is syntax-valid Python | 4 Marks |
| **TC2** | Parses error logs and normalizes dynamic IDs/timestamps | 4 Marks |
| **TC3** | Groups identical error signatures into clusters | 4 Marks |
| **TC4** | Writes structured JSON output to error_clusters.json | 4 Marks |
| **TC5** | Matches cluster signature to runbook ID | 3 Marks |
| **TC6** | Calculates error frequency per cluster | 2 Marks |
| **TC7** | Handles missing/malformed log lines gracefully | 2 Marks |
| **TC8** | Includes first and last occurrence timestamps | 2 Marks |

**Total Score: 25 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
