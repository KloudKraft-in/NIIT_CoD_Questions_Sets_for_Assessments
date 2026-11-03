# Basic Code Analysis: Fixing Common Runtime Error Patterns

Duration : 30 Min.

## Scenario
A critical report generation function fails dynamically when database record fields are omitted. Resolve the undefined property reference.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/app.js`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Refactor the file 'report_generator.js' to add safe undefined-fallback checks.

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
| **TC1** | report_generator.js is syntax-valid JS | 3 Marks |
| **TC2** | Checks present for missing field properties | 4 Marks |
| **TC3** | Returns fallback string when fields are null/undefined | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
