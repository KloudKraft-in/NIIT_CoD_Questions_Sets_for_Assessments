# GenAI Ops: Indirect Prompt Injection Defense & Log Poisoning Firewall

Duration : 90 Min.

## Scenario
Build a log pre-processor firewall script ('log_firewall.py') that scans production logs, detects embedded prompt injection vectors, and outputs a clean dataset.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/log_firewall.py`
**Input Resource File to Inspect**: `student_workspace/production_stream.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `production_stream.log` in `student_workspace/`.
- Create or update `student_workspace/log_firewall.py` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `chat_history.json` inside `student_workspace/`.
3. Create or open `student_workspace/log_firewall.py` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | log_firewall.py is syntax-valid Python | 3 Marks |
| **TC2** | Detects 'Ignore previous instructions' injection vector | 3 Marks |
| **TC3** | Detects 'System:' / '[INSTRUCTION]' role hijacking attempts | 3 Marks |
| **TC4** | Strips injection payloads while preserving real log lines | 3 Marks |
| **TC5** | Outputs sanitized_logs.json | 2 Marks |
| **TC6** | Generates security audit log entry for blocked injections | 2 Marks |
| **TC7** | Calculates log sanitization statistics | 2 Marks |
| **TC8** | Handles high-throughput log streams efficiently | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
