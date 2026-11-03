# .NET Lab: IIS App Pool Overlapping Recycle Config

Duration : 50 Min.

## Scenario
A website suffers connection timeouts during pool recycling due to simultaneous process termination without overlap.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Write configure_recycle.ps1 to configure the IIS site App Pool to use overlapping recycle and set idle timeout to zero.

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
| **TC2** | File configure_recycle.ps1 exists | 3 Marks |
| **TC3** | Script references App Pool name 'SalesPool' | 3 Marks |
| **TC4** | Script sets disallowOverlappingRecycle property to False | 3 Marks |
| **TC5** | Script configures idleTimeout time span to 0 | 3 Marks |
| **TC6** | Specific time based recycle triggers disabled | 2 Marks |
| **TC7** | Logging for recycling events configured | 2 Marks |
| **TC8** | Rapid Fail Protection limit set to 5 | 2 Marks |
| **TC9** | PowerShell syntax checks pass | 2 Marks |

**Total Score: 20 Marks**
