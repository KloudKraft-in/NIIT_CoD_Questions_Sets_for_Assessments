# .NET Lab: Docker Multi-Stage Build and Publish

Duration : 30 Min.

## Scenario
To optimize docker container sizes, a multi-stage Dockerfile must be written to build and deploy the ASP.NET Core application.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Complete the Dockerfile in the workspace root using SDK and runtime tags for .NET 8.

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
| **TC2** | Dockerfile exists in workspace root | 5 Marks |
| **TC3** | Multi-stage uses mcr.microsoft.com/dotnet/sdk:8.0 as build | 5 Marks |
| **TC4** | Build stage executes dotnet publish command | 5 Marks |
| **TC5** | Final runtime stage uses mcr.microsoft.com/dotnet/aspnet:8.0 | 5 Marks |

**Total Score: 20 Marks**
