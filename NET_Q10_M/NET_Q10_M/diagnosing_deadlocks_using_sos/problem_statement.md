# .NET Lab: Diagnosing deadlocks using SOS

Duration : 60 Min.

## Scenario
A production Web API application hangs under load. Thread stack diagnostics indicate a managed deadlock.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Capture a process memory dump, import SOS debugging symbols, run sync block commands to locate deadlock ownership, and write a code fix.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Managed process memory dump capture execution log: 2.5 marks
2. SOS debugging extension initialization verification: 2.5 marks
3. Identify blocked threads execution stack frames: 2.5 marks
4. Extract sync block owner monitors addresses: 2.5 marks
5. Locate deadlock loop candidate thread IDs: 2.5 marks
6. Isolate lock resource code lines in repositories: 2.5 marks
7. Asynchronous lock boundaries code patch implementation: 2.5 marks
8. Thread pool recovery validation metrics: 2.5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
