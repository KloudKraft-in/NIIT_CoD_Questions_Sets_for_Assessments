# JVM Lab: JVM Deadlock & Contention Analysis

Duration : 30 Min.

## Scenario
A multi-threaded processing application hangs randomly. You need to gather JVM diagnostics to identify lock contentions and propose a resolution.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Capture thread dumps using jcmd or jstack, locate the BLOCKED state threads, identify the deadlocked monitor lock, and document the lock refactoring recommendation.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Thread dump capture command logs execution: 5 marks
2. Deadlock thread monitors identification and recommended lock refactoring: 5 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
