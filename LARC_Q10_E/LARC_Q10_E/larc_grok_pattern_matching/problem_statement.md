# Log Analysis: Grok Pattern Field Extraction

Duration : 30 Min.

## Scenario
An Logstash ingestion pipeline needs a custom Grok pattern to parse Apache access logs. Construct a valid Grok pattern.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/grok_pattern.txt`
**Input Resource File to Inspect**: `student_workspace/nginx_access.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `nginx_access.log` in `student_workspace/`.
- Edit `grok_pattern.txt` and record the required log analytics or findings.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `nginx_access.log` inside `student_workspace/`.
3. Open `grok_pattern.txt` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | grok_pattern.txt exists | 3 Marks |
| **TC2** | %{IP:clientip} or %{IPV4:clientip} pattern included | 4 Marks |
| **TC3** | %{NUMBER:status} or %{INT:status} pattern included | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
