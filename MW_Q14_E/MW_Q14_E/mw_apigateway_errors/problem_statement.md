# Middleware Lab: API Gateway Error Code Classification

Duration : 45 Min.

## Scenario
An API Gateway fronting a billing service returns HTTP 401 and 504 errors during seasonal transaction surges.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Build a diagnostic runbook classifying gateway-level HTTP statuses and map responsibilities to downstream support teams.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Classifying client-side errors (401, 403, 404) and identifying owner teams: 3 marks
2. Classifying server-side errors (500, 502, 504) and identifying owner teams: 3 marks
3. Setting custom HTTP response bodies for API Gateway failure states: 4 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
