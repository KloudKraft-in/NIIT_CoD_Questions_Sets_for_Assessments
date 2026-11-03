# Log Analysis: W3C & GELF Structured Log Format Validation

Duration : 30 Min.

## Scenario
A Graylog ingest pipeline is rejecting incoming logs. Audit W3C and GELF log format specifications to fix invalid field types.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/gelf_log.json`
**Input Resource File to Inspect**: `student_workspace/w3c_access.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `w3c_access.log` in `student_workspace/`.
- Edit `gelf_log.json` and record the required log analytics or findings.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `w3c_access.log` inside `student_workspace/`.
3. Open `gelf_log.json` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | gelf_log.json has valid JSON schema | 3 Marks |
| **TC2** | Mandatory '_host' and 'short_message' fields present | 4 Marks |
| **TC3** | Numeric syslog level specified correctly | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
