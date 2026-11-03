# Basic Code Analysis: Repairing Maven Dependency Conflict Warnings

Duration : 45 Min.

## Scenario
A Java application crashes at boot with a NoSuchMethodError due to duplicate Jackson core dependencies. Exclude duplicate library dependencies inside pom.xml.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/pom.xml`
**Input Resource File to Inspect**: `student_workspace/pom.xml`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Edit 'pom.xml' to add exclusions under the conflicting dependency block.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `pom.xml` inside `student_workspace/`.
3. Open `pom.xml` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | pom.xml contains valid XML | 3 Marks |
| **TC2** | Conflicting jackson library correctly excluded | 3 Marks |
| **TC3** | Correct exclusion schema syntax used | 2 Marks |
| **TC4** | Main dependencies remain intact | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
