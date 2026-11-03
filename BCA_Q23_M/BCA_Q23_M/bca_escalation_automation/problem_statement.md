# Basic Code Analysis: Automating Service Incident Escalations

Duration : 90 Min.

## Scenario
You need to write a script that parses incident alerts from a log file, matches them to service owners via metadata records, and generates an escalation report file.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/escalate.py`
**Input Resource File to Inspect**: `student_workspace/escalate.py`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Complete the Python script 'escalate_incident.py' to read alerts and write the report to 'escalation_report.json'.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `escalate.py` inside `student_workspace/`.
3. Open `escalate.py` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | escalate_incident.py is syntax-valid Python | 3 Marks |
| **TC2** | Correctly parses alert status codes and log exceptions | 3 Marks |
| **TC3** | Finds correct team mapping entries | 3 Marks |
| **TC4** | Writes valid JSON output to escalation_report.json | 3 Marks |
| **TC5** | Includes stack trace summary logs | 2 Marks |
| **TC6** | Escalates high severity to immediate manager channel | 2 Marks |
| **TC7** | Handles file read/write exceptions | 2 Marks |
| **TC8** | Correctly formats escalation timestamps | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
