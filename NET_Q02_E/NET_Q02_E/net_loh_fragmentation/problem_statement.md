# .NET Lab: LOH Threshold Configuration

Duration : 30 Min.

## Scenario
An API processing large payloads suffers from performance degradation due to LOH fragmentation and frequent Gen 2 GCs.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure runtimeconfig.json to enable Server GC and define Large Object Heap limits, and document the heap compaction settings.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. runtimeconfig.json GC execution mode properties setup: 5 marks
2. Large Object Heap (LOH) threshold allocations check: 5 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
