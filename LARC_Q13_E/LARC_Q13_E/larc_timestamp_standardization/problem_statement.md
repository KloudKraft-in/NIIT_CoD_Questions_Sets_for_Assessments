# Log Analysis: ISO 8601 & Unix Epoch Timestamp Standardization

Duration : 45 Min.

## Scenario
A log aggregator receives timestamps in mixed formats (Unix Epoch, ISO 8601, EST local time). Standardize all timestamps to ISO 8601 UTC format.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/timestamp_converter.js`
**Input Resource File to Inspect**: `student_workspace/mixed_timestamps.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `mixed_timestamps.log` in `student_workspace/`.
- Edit `timestamp_converter.js` and record the required log analytics or findings.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `mixed_timestamps.log` inside `student_workspace/`.
3. Open `timestamp_converter.js` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | timestamp_converter.js is syntax-valid JS | 3 Marks |
| **TC2** | Unix epoch converted to ISO string correctly | 3 Marks |
| **TC3** | Local timezone offsets adjusted to UTC Z format | 2 Marks |
| **TC4** | Returns string ending with 'Z' or '+00:00' | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
