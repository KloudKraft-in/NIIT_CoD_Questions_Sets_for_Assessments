# Basic Code Analysis: Service Ownership & Module Mapping

Duration : 30 Min.

## Scenario
An incident alert is raised in the billing service. You must look up the service metadata registry to identify the responsible engineering team and contact slack channel.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/billing_service.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Populate contact details for the owner team of 'billing-service' in your 'solution.json'.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `billing_service.log` inside `student_workspace/`.
3. Open `solution.json` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | solution.json exists | 3 Marks |
| **TC2** | Correct team name mapped | 4 Marks |
| **TC3** | Correct contact slack channel mapped | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
