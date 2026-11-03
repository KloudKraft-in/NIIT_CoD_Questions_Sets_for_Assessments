# Node.js Lab: Event Loop Latency Monitor

Duration : 30 Min.

## Scenario
A performance monitoring platform requires raw metrics from the event loop execution loop to alert engineers of event-loop blockages.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Implement an event loop lag monitor inside `monitor.js` using native perf_hooks `monitorEventLoopDelay` utility, tracking statistical percentiles and writing them when requested.

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
| **TC1** | Module imports monitorEventLoopDelay helper function from perf_hooks | 5 Marks |
| **TC2** | Stats reporting helper exports valid lag percentiles calculations | 5 Marks |

**Total Score: 10 Marks**
