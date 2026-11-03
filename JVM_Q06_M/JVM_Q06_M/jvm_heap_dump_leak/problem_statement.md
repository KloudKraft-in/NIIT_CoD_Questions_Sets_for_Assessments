# JVM Lab: JVM Memory Leak Investigation

Duration : 60 Min.

## Scenario
A long-running task processor crashes with OutOfMemoryError: Java heap space after 4 hours of operations. A memory leak is suspected.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Analyze the provided heap dump (.hprof) using Eclipse MAT, isolate the leaking objects path to GC Roots, identify the target static map retention leak, and implement a fix.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Heap dump parsing command logs verification: 5 marks
2. Leaky collection paths to GC Roots identification: 5 marks
3. Static map retention leaks suspects profiling report: 5 marks
4. Code-level remediation code fix implementation: 5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
