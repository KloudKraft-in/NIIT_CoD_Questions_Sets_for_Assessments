# Basic Code Analysis: Advanced Incident RCA Audit Logging

Duration : 90 Min.

## Scenario
Analyze a multi-system failure involving a network gateway timeout and a database deadlock, classify the issues, and generate a structured post-mortem log.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/outage_trace.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Fill out 'solution.json' detailing the incident correlation timeline and classification category.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. To initialize the environment log file, run `python setup_git.py` in the terminal inside `student_workspace/` (or inspect `outage_trace.log`).
3. Open and inspect `outage_trace.log` inside `student_workspace/`.
4. Open `solution.json` in `student_workspace/` and perform the required modifications.
5. Save your changes (`Ctrl + S` or `Cmd + S`).
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | solution.json exists and is valid JSON | 4 Marks |
| **TC2** | Primary classification mapped to INTEGRATION/INFRA | 4 Marks |
| **TC3** | Deadlock trigger transaction correctly identified | 4 Marks |
| **TC4** | Gateway timeout duration correctly calculated | 4 Marks |
| **TC5** | Correlation ID matched | 3 Marks |
| **TC6** | Post-mortem timeline entries are sequential | 2 Marks |
| **TC7** | Mitigation steps are documented | 2 Marks |
| **TC8** | Severity level correctly identified | 2 Marks |

**Total Score: 25 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
