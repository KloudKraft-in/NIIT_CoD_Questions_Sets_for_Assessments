# Node.js Lab: Memory Leak Diagnostics

Duration : 60 Min.

## Scenario
An Express application endpoint `/api/track` accumulates client metadata in a global data structure without eviction, resulting in an active memory leak.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Identify the leaky array/collection pattern inside `server.js` and restrict cache sizing to a maximum threshold of 100 elements using Map eviction.

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
| **TC1** | File server.js exists in workspace | 5 Marks |
| **TC2** | Leaking array resolved or replaced with size-limited collection | 5 Marks |
| **TC3** | Express routes perform successfully under load | 5 Marks |
| **TC4** | Memory heap consumption verified to remain bounded | 5 Marks |

**Total Score: 20 Marks**
