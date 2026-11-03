# GenAI Ops: Recognizing AI Hallucinations in CLI Commands

Duration : 30 Min.

## Scenario
An AI assistant generated a list of Linux bash commands for troubleshooting. Review the list, detect fabricated CLI flags, and extract non-existent commands.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/command_audit.json`
**Input Resource File to Inspect**: `student_workspace/ai_suggested_commands.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `ai_suggested_commands.txt` in `student_workspace/`.
- Create or update `student_workspace/command_audit.json` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `ai_suggested_commands.txt` inside `student_workspace/`.
3. Create or open `student_workspace/command_audit.json` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | command_audit.json exists | 3 Marks |
| **TC2** | Fabricated flag '--force-push-all' identified | 4 Marks |
| **TC3** | Non-existent command 'sysclean-all' marked as hallucinated | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
