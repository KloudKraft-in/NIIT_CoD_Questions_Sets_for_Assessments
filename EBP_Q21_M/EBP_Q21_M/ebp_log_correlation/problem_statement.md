# Enterprise Batch Lab: Log Correlation & RCA Auditing

Duration : 90 Min.

## Scenario
A critical transaction batch fails. Operations must correlate logs across the web frontend, Spring Batch runner, and Oracle database to generate a Root Cause Analysis (RCA).

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Parse multi-system logs using unique transaction execution IDs to locate the exception.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Filtering multi-system log streams by execution ID: 3 marks
2. Mapping event timestamps across distinct cluster nodes: 3 marks
3. Locating database deadlock exceptions in DB system logs: 3 marks
4. Tracing JVM out-of-memory errors in batch execution logs: 3 marks
5. Isolating code-level stack trace exceptions: 2 marks
6. Evaluating database locks status tables reports: 2 marks
7. Documenting correlation findings and timeline: 2 marks
8. Recommending database index changes to prevent OOM errors: 2 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
