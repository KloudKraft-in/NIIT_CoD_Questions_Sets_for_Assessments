# GenAI Ops: Data Privacy & PII Log Sanitization

Duration : 30 Min.

## Scenario
Application logs contain sensitive PII (SSNs, API keys, Passwords) before being sent to an external AI service. Sanitize the logs while preserving error context.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/sanitized_log.json`
**Input Resource File to Inspect**: `student_workspace/raw_application_logs.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `raw_logs.txt` in `student_workspace/`.
- Create or update `student_workspace/sanitized_log.json` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `raw_logs.txt` inside `student_workspace/`.
3. Create or open `student_workspace/sanitized_log.json` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | sanitized_log.json exists and contains sanitized_log key | 3 Marks |
| **TC2** | All SSNs and API keys masked with [REDACTED] | 4 Marks |
| **TC3** | Non-sensitive stack trace lines preserved | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
