# Basic Code Analysis: Configuring Spring Profiles in YAML format

Duration : 45 Min.

## Scenario
A deployment workflow fails to activate the production credentials because of dynamic profile property resolving issues in application.yml.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/application.yml`
**Input Resource File to Inspect**: `student_workspace/application.yml`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure Spring Boot multi-profile configuration settings in 'application.yml'.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `application.yml` inside `student_workspace/`.
3. Open `application.yml` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | application.yml has valid YAML structure | 3 Marks |
| **TC2** | spring.profiles.active variable configured correctly | 3 Marks |
| **TC3** | Different properties defined under 'prod' divider blocks | 2 Marks |
| **TC4** | Correct indentation spacing in configuration nodes | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
