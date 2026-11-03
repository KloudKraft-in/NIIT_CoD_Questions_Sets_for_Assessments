# Basic Code Analysis: Auditing Spring properties files

Duration : 30 Min.

## Scenario
A Spring Boot microservice fails to run in Dev environment because database profiles are mismatched. Audit the config files.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/application.properties`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Correct active profile properties and database URLs inside 'application.properties'.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `application.properties` inside `student_workspace/`.
3. Open `solution.json` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | application.properties has valid Spring boot keys | 3 Marks |
| **TC2** | Active profile set to 'dev' | 4 Marks |
| **TC3** | Database URL port set to local container port 3306 | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
