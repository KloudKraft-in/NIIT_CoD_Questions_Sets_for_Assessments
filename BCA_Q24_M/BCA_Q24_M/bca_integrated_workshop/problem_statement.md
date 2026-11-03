# Basic Code Analysis: Integrated Outage Troubleshooting Workshop

Duration : 90 Min.

## Scenario
A major production crash occurred in the checkout cluster. Correlate Apache logs, Java Spring exceptions, database deadlocks, and configuration properties. Identify the root cause and draft a developer-ready post-mortem.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/outage_trace.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Fill out 'post_mortem_report.json' in your workspace.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `outage_trace.log` inside `student_workspace/`.
3. Open `solution.json` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | post_mortem_report.json exists and is valid JSON | 4 Marks |
| **TC2** | Root cause correctly identified as database connection pool exhaustion | 4 Marks |
| **TC3** | Mismatched environment property config parameter mapped correctly | 4 Marks |
| **TC4** | File name, class, and method of leak suspect correct | 4 Marks |
| **TC5** | Outage timeline (start/end) correctly parsed from log lines | 3 Marks |
| **TC6** | Business impact metrics correctly logged | 2 Marks |
| **TC7** | Immediate recovery steps documented | 2 Marks |
| **TC8** | Long-term architectural remediations included | 2 Marks |

**Total Score: 25 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
