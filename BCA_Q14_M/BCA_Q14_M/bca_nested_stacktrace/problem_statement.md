# Basic Code Analysis: Complex Nested Stack Trace Diagnostics

Duration : 60 Min.

## Scenario
A multithreaded transaction gateway fails under stress. Deeply examine the nested stack trace logs to find the root cause database exception.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/nested_stacktrace.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Fill out 'solution.json' detailing the nested exception layer stack frames.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `nested_stacktrace.log` inside `student_workspace/`.
3. Open `solution.json` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | solution.json exists and is valid JSON | 5 Marks |
| **TC2** | Root exception correctly identified as SqlException | 5 Marks |
| **TC3** | Deadlock error code (1205) correctly located in log trace | 5 Marks |
| **TC4** | Class name of blocking query correctly mapped | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
