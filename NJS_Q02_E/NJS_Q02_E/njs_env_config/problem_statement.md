# Node.js Lab: Node.js Environment Configuration

Duration : 30 Min.

## Scenario
A deployment pipeline crashes because the Node.js application attempts to connect using wrong or missing environment properties.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Write a script `config.js` that reads PORT, NODE_ENV, and DB_URL from environment variables, sets defaults if missing, and writes a verified JSON config metadata report to `config_report.json`.

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
| **TC1** | File config.js exists and runs successfully | 5 Marks |
| **TC2** | JSON report config_report.json is correctly generated | 5 Marks |

**Total Score: 10 Marks**
