# JVM Lab: JVM Metaspace OutOfMemory incident

Duration : 120 Min.

## Scenario
A production service dynamically loading classes crashes with OutOfMemoryError: Metaspace. You must diagnose and resolve the incident.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Analyze crash dumps, identify dyn-class loading leaks, tune Metaspace parameters (-XX:MaxMetaspaceSize), and write a post-mortem incident report.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. OutOfMemory scenario reproduction setup: 2.5 marks
2. Metaspace vs Heap memory bounds profiling configurations: 2.5 marks
3. Dynamic class loader reflection leaks trace extraction: 2.5 marks
4. Process dumps generation command execution logs: 2.5 marks
5. Memory consumer instances and counts profiling report: 2.5 marks
6. Garbage collection performance overheads metrics logs: 2.5 marks
7. Architectural prevention and sizing limits recommendations: 2.5 marks
8. Production incident post-mortem escalation handoff report: 2.5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
