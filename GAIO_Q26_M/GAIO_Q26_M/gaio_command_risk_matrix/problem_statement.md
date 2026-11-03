# GenAI Ops: Automated Command Risk Assessment Matrix

Duration : 90 Min.

## Scenario
Build a Python security filter ('command_guard.py') that evaluates AI-suggested bash commands against a production safety matrix before execution.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/command_guard.py`
**Input Resource File to Inspect**: `student_workspace/untrusted_bash_commands.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `untrusted_bash_commands.txt` in `student_workspace/`.
- Create or update `student_workspace/command_guard.py` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `untrusted_bash_commands.txt` inside `student_workspace/`.
3. Create or open `student_workspace/command_guard.py` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | command_guard.py is syntax-valid Python | 3 Marks |
| **TC2** | Flags destructive commands (rm -rf, dd, mkfs) | 3 Marks |
| **TC3** | Flags privileged escalation (sudo su, chmod 777) | 3 Marks |
| **TC4** | Allows read-only diagnostic commands (cat, grep, ps) | 3 Marks |
| **TC5** | Assigns risk score (LOW, MEDIUM, HIGH, CRITICAL) | 2 Marks |
| **TC6** | Outputs risk_assessment.json | 2 Marks |
| **TC7** | Includes remediation recommendation | 2 Marks |
| **TC8** | Handles empty/malformed command input gracefully | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
