# GenAI Ops: Production Operational Verification & Safe Execution

Duration : 30 Min.

## Scenario
Before running AI-suggested commands in production, perform safety verification. Categorize commands into SAFE, NEEDS_REVIEW, or NEVER_RUN.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/prod_commands_list.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `prod_commands_list.txt` in `student_workspace/`.
- Create or update `student_workspace/solution.json` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `prod_commands_list.txt` inside `student_workspace/`.
3. Create or open `student_workspace/solution.json` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | solution.json exists | 3 Marks |
| **TC2** | 'rm -rf /' marked as NEVER_RUN | 4 Marks |
| **TC3** | 'kubectl get pods' marked as SAFE | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
