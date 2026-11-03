# .NET Lab: Automated IIS Site Bindings

Duration : 30 Min.

## Scenario
Deploying apps to IIS requires setting up site bindings and Application Pool associations via PowerShell scripting.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Complete configure_iis.ps1 to create an IIS website bound to port 8085 with target name 'SalesPortal'.

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
| **TC1** | Local VM Environment active and verified | 0 Marks |
| **TC2** | File configure_iis.ps1 exists in the workspace | 5 Marks |
| **TC3** | Script uses the New-IISSite or New-Website command name | 5 Marks |
| **TC4** | Website name is configured as 'SalesPortal' | 5 Marks |
| **TC5** | Binding port is set to 8085 | 5 Marks |

**Total Score: 20 Marks**
