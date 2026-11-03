# .NET Lab: ASP.NET Core Middleware Exceptions

Duration : 30 Min.

## Scenario
Your Web API crashes under unhandled exceptions, returning standard stack trace leaks to client responses.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Implement custom ASP.NET Core exception middleware that intercepts all errors, returns RFC 7807 problem details payloads, and writes structured log records.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Custom exception handling middleware class implementation: 5 marks
2. RFC 7807 problem details response formatting and logging check: 5 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
