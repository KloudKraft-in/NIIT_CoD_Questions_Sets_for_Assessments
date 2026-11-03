# Basic Code Analysis: Git History & Blame Navigation

Duration : 30 Min.

## Scenario
A bug was introduced in the user registration flow. You need to analyze the Git commit history of a mock repository and identify the commit hash and author that modified the signup validation rule.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/app.js`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Fill in the correct commit hash and author username inside 'solution.json' in your workspace.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `app.js` inside `student_workspace/`.
3. Open `solution.json` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | solution.json exists and is valid JSON | 3 Marks |
| **TC2** | Correct commit hash identified | 4 Marks |
| **TC3** | Correct author username identified | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
