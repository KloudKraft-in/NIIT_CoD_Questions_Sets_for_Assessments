# .NET Lab: Refactoring ASP.NET Core Middleware Pipeline Execution Order

Duration : 35 Min.

## Scenario
Security scanning highlights that static files are served without authentication checks. The middleware pipeline registration order is incorrect.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Refactor registration sequence in Program.cs to execute UseAuthentication and UseAuthorization before UseStaticFiles to ensure static files require authentication.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Local VM Environment active and verified | 0 Marks |
| **TC2** | Program.cs exists in workspace | 5 Marks |
| **TC3** | UseAuthentication is registered before UseStaticFiles | 5 Marks |
| **TC4** | UseAuthorization is registered before UseStaticFiles | 5 Marks |
| **TC5** | Middleware pipeline order is correct and executes cleanly | 5 Marks |

**Total Score: 20 Marks**
