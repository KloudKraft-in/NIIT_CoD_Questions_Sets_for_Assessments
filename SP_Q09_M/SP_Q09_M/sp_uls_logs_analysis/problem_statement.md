# SharePoint Lab: ULS Logs Troubleshooting

Duration : 60 Min.

## Scenario
A SharePoint farm page is rendering an HTTP 500 error page with a Correlation ID. You must search the ULS logs to locate the exception stack trace.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Analyze ULS log files using PowerShell cmdlets and identify root causes of Correlation ID exceptions.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Filtering ULS log entries by Correlation ID: 5 marks
2. Parsing log levels (Critical/Error) to find exception: 5 marks
3. Isolating database/code execution call stack details: 5 marks
4. Documenting root cause and remediation recommendations: 5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
