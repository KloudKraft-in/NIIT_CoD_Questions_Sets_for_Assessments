# Log Analysis: Enterprise Splunk SPL Aggregations & Transactions

Duration : 90 Min.

## Scenario
An enterprise web portal experienced high latency. Write Splunk SPL queries using `stats` and `transaction` commands to calculate average response time per endpoint.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/splunk_logs.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `splunk_logs.txt` in `student_workspace/`.
- Edit `solution.json` and record the required log analytics or findings.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `splunk_logs.txt` inside `student_workspace/`.
3. Open `solution.json` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | solution.json exists | 5 Marks |
| **TC2** | Splunk 'stats avg(response_time)' aggregation query correct | 5 Marks |
| **TC3** | 'transaction session_id' grouping command included | 5 Marks |
| **TC4** | 'by endpoint' clause specified | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
