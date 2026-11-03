# Node.js Lab: Event Loop Phase Execution Order

Duration : 30 Min.

## Scenario
A Node.js microservice produces out-of-order execution side-effects because of misunderstandings regarding microtask and macrotask execution phases.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Write a script `index.js` that schedules callbacks using nextTick, resolved promise, setTimeout, and setImmediate to output specific log messages demonstrating Node.js Event Loop phases execution order.

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
| **TC1** | File index.js exists and compiles cleanly | 5 Marks |
| **TC2** | Execution output order matches Event Loop phase priorities | 5 Marks |

**Total Score: 10 Marks**
