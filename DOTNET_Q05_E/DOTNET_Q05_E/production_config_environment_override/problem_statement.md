# .NET Lab: Production Config Environment Override

Duration : 20 Min.

## Scenario
The database connection settings must be isolated between environment config layers.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure appsettings.Production.json to define a database connection string with server target 'prod-db'.

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
| **TC2** | File appsettings.Production.json exists | 4 Marks |
| **TC3** | Configuration file compiles as valid JSON | 3 Marks |
| **TC4** | Production ConnectionString uses server 'prod-db' | 3 Marks |

**Total Score: 10 Marks**
