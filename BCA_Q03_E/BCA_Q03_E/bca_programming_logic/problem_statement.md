# Basic Code Analysis: Spotting Logical & Null Errors

Duration : 30 Min.

## Scenario
An application is crashing with a Null Pointer Exception when looking up non-existent user IDs. Inspect the provided JavaScript snippet and fix the boundary check.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/user_lookup.js`
**Input Resource File to Inspect**: `student_workspace/user_lookup.js`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Edit 'user_lookup.js' to add a check for undefined/null user objects before referencing '.profile.email'.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `user_lookup.js` inside `student_workspace/`.
3. Open `user_lookup.js` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | user_lookup.js contains syntax-valid JS code | 3 Marks |
| **TC2** | Code handles non-existent/null user objects correctly | 4 Marks |
| **TC3** | Function returns an empty string or null instead of throwing an error | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
