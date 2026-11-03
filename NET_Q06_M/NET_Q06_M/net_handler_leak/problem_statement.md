# .NET Lab: Event Handler Memory Leak

Duration : 60 Min.

## Scenario
A Windows service or long-running worker experiences memory growth. Analysis points to managed objects being kept alive unexpectedly.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Use SOS commands to diagnose memory leaks from event handler strong subscriptions, refactor using WeakEventManager or explicit unsubscriptions, and verify memory footprint stability.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. SOS debugging commands memory leak diagnostics logs: 5 marks
2. Event handlers strong references unsubscriptions patch: 5 marks
3. WeakEventManager refactoring logic verification: 5 marks
4. Load test memory stability and heap metrics verification: 5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
