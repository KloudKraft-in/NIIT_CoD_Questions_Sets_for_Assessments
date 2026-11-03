# Enterprise Batch Lab: Troubleshooting Spring Batch Job Repositories

Duration : 30 Min.

## Scenario
A Spring Batch job fails to restart because the previous failed execution was not flagged correctly in the metadata repository tables.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Verify the state of standard Spring Batch tables (e.g., BATCH_JOB_EXECUTION, BATCH_STEP_EXECUTION) and write metadata corrections.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Querying Spring Batch metadata tables to extract failed statuses: 3 marks
2. Formulating step-execution override parameters to allow restarts: 3 marks
3. Adjusting Execution Context keys to prevent duplicate runs: 4 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
