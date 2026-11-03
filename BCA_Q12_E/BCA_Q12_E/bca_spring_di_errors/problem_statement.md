# Basic Code Analysis: Resolving Spring Bean Creation Failures

Duration : 30 Min.

## Scenario
A Spring app crashes with 'NoSuchBeanDefinitionException' for UserService. Inspect class decorators and configure annotations.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/spring_di.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Add missing '@Service' annotation to 'UserService.java' to register it inside Spring's context.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `spring_di.log` inside `student_workspace/`.
3. Open `solution.json` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | UserService.java exists and is syntax-valid | 3 Marks |
| **TC2** | @Service or @Component annotation added | 4 Marks |
| **TC3** | @Autowired or constructor injection configured correctly | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
