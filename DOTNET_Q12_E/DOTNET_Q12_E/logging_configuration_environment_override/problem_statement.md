# .NET Lab: Logging Configuration Environment Override

Duration : 30 Min.

## Scenario
Logging targets must be overridden in container pipelines using standard environment patterns.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Write a bash/batch script override_env.sh or override_env.bat that sets the ASP.NET Core environment variable for Default LogLevel to Warning.

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
| **TC2** | File override_env.sh or override_env.bat exists in the workspace | 5 Marks |
| **TC3** | Script sets the environment variable ASPNETCORE_ENVIRONMENT to Production | 5 Marks |
| **TC4** | Script defines Logging__LogLevel__Default override key | 5 Marks |
| **TC5** | Default log level override value is set to Warning | 5 Marks |

**Total Score: 20 Marks**
