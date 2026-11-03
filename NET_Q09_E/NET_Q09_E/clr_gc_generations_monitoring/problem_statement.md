# .NET Lab: CLR GC Generations Monitoring

Duration : 30 Min.

## Scenario
To optimize runtime memory profiles, you must trace managed allocations and verify how objects promote between CLR generations.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure dotnet-counters to trace Gen 0, 1, 2 collections. Run a memory allocation load loop, capture GC triggers metadata, and output a JSON diagnostics metric summary.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. CLR profiling counters execution validation setup: 2 marks
2. Gen 0 heap size and collection rates extraction: 2 marks
3. Gen 1 promotion frequency metrics capture: 2 marks
4. Gen 2 collections and Full GC boundaries validation: 2 marks
5. Tuned garbage collections memory footprint baseline report: 2 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
