# Node.js Lab: Async/Await Parallel Processing Flow

Duration : 30 Min.

## Scenario
An integration gateway makes external HTTP calls in a loop sequentially. This serial execution blocks API responses, resulting in timeouts under load.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Refactor the fetchUrls method in `fetcher.js` to execute independent promises concurrently using Promise.all to optimize system throughput.

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
| **TC1** | File fetcher.js exists in student workspace | 2 Marks |
| **TC2** | Module compiles and exports fetchUrls method | 2 Marks |
| **TC3** | Method fetchUrls correctly resolves array output data | 2 Marks |
| **TC4** | Parallel execution reduces latency compared to sequential run | 2 Marks |
| **TC5** | Code uses native Promise.all to achieve concurrency | 2 Marks |

**Total Score: 10 Marks**
