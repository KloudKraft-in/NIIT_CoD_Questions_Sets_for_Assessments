# Node.js Lab: Automated Heap Snapshots

Duration : 60 Min.

## Scenario
To diagnose transient memory leak spikes, the SRE team requires an automated process monitor that generates heap snapshots when memory usage surges.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Implement an automated polling checker in `diagnostics.js` that checks memory utilization and calls `v8.writeHeapSnapshot()` if RSS exceeds 200MB.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | File diagnostics.js exists and runs successfully | 5 Marks |
| **TC2** | V8 write heap snapshot native helper is integrated | 5 Marks |
| **TC3** | Heap snapshot triggers at correct threshold limit | 5 Marks |
| **TC4** | Dumps saved with timestamp details to target directories | 5 Marks |

**Total Score: 20 Marks**
