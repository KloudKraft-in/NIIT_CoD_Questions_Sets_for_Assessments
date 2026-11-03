# Node.js Lab: Express.js Exception Boundaries

Duration : 30 Min.

## Scenario
An Express.js web service crashes unexpectedly in production because async route handlers lack proper error catch boundaries, and global unhandled promise rejections are not intercepted.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Set up global process exception boundaries for uncaughtException and unhandledRejection events in `server.js` and wrap Express async endpoints in error handlers.

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
| **TC1** | Global uncaughtException and unhandledRejection event listeners are registered | 5 Marks |
| **TC2** | Application error boundaries route async exceptions safely | 5 Marks |

**Total Score: 10 Marks**
