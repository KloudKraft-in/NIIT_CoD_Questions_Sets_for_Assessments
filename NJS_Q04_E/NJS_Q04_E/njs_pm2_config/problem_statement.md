# Node.js Lab: PM2 Cluster Configuration

Duration : 30 Min.

## Scenario
To optimize container resource usage and enable high availability, you need to configure a PM2 process manager config file.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Build a PM2 ecosystem file named `ecosystem.config.js` running in cluster mode with 2 instances, max memory auto-restart limit of 150MB, and custom log output file paths.

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
| **TC1** | PM2 ecosystem.config.js exists and exports a valid configuration | 5 Marks |
| **TC2** | Cluster execution mode, instances, and memory restart threshold correctly set | 5 Marks |

**Total Score: 10 Marks**
