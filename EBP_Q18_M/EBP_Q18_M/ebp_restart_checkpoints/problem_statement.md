# Enterprise Batch Lab: Configuring Spring Batch Chunk Restart Checkpoints

Duration : 90 Min.

## Scenario
A spring batch step processing 1 million records fails halfway. You must configure checkpoint chunk restarts to resume from the last committed chunk.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure reader state persistence and savepoint transaction intervals inside the Spring Batch XML/Java configuration.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Configuring chunk reader state saving (SaveState) properties: 3 marks
2. Optimizing chunk size commit intervals to match SLA windows: 3 marks
3. Setting database transaction savepoint boundaries: 3 marks
4. Designing job execution skip/retry exceptions parameters: 3 marks
5. Setting item processor error filters: 2 marks
6. Resolving database deadlocks via retry configurations: 2 marks
7. Documenting recovery checkpoint validation steps: 2 marks
8. Implementing custom step listeners to log checkpoint steps: 2 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
