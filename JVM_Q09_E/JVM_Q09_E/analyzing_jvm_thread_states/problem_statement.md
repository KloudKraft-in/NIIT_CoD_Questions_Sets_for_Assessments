# JVM Lab: Analyzing JVM Thread States

Duration : 30 Min.

## Scenario
A transaction logging system experiences locks degradation, resulting in threads blocking. You need to capture runtime dumps and isolate thread state boundaries.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Isolate thread states in thread dumps. Identify threads blocked in RUNNABLE, WAITING, and BLOCKED phases, mapping monitor locks in the workspace config report.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Capture thread dump state using JDK diagnostic commands: 2 marks
2. Identify threads residing in RUNNABLE execution phases: 2 marks
3. Isolate threads locked in WAITING/TIMED_WAITING monitors: 2 marks
4. Identify thread IDs in BLOCKED sync boundaries: 2 marks
5. Propose resource contention refactoring steps: 2 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
