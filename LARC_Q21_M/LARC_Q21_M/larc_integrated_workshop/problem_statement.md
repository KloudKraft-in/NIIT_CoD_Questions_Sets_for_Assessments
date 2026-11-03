# Log Analysis: Integrated Log Investigation Workshop (End-to-End Incident Triage)

Duration : 90 Min.

## Scenario
A major production outage affected the payment gateway. Correlate Linux auth/syslog logs, Java Spring stack traces, Splunk search results, and correlation IDs to perform root cause analysis and generate a structured incident report.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/outage_trace.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `outage_trace.log` in `student_workspace/`.
- Edit `solution.json` and record the required log analytics or findings.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `outage_trace.log` inside `student_workspace/`.
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
| **TC1** | solution.json exists and is valid JSON | 4 Marks |
| **TC2** | Root cause correctly identified as database connection pool exhaustion | 4 Marks |
| **TC3** | Primary correlation ID ('corr-9921') matched across logs | 4 Marks |
| **TC4** | Failing microservice class and method line number mapped | 4 Marks |
| **TC5** | Outage duration and impact metrics correctly calculated | 3 Marks |
| **TC6** | Log evidence snippet included | 2 Marks |
| **TC7** | Immediate recovery actions documented | 2 Marks |
| **TC8** | Long-term architectural remediations included | 2 Marks |

**Total Score: 25 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
