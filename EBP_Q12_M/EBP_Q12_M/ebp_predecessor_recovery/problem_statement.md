# Enterprise Batch Lab: Complex Dependent Job Predecessor Recovery

Duration : 60 Min.

## Scenario
A main inventory update batch job fails at Step 3 of 10. Downstream pricing databases cannot load old inventories. You need to repair the state and resume the flow.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Document the steps to force success status, restore predecessor checkpoint databases, and safely bypass non-critical checkpoints.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Restoring databases to matching pre-step checkpoint states: 5 marks
2. Forcing job statuses safely inside Control-M/AutoSys schedulers: 5 marks
3. Ensuring downstream database integrity and transaction consistency: 5 marks
4. Conducting verification checks prior to resuming downstream jobs: 5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
