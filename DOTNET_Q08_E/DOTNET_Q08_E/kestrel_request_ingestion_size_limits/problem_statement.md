# .NET Lab: Kestrel Request Ingestion Size limits

Duration : 25 Min.

## Scenario
To mitigate Denial-of-Service attacks, Kestrel limits must restrict the maximum request size payload.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure appsettings.json to set the Kestrel Limits MaxRequestBodySize parameter to 10MB (10,485,760 bytes).

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
| **TC2** | File appsettings.json exists in the workspace | 4 Marks |
| **TC3** | MaxRequestBodySize is configured inside Kestrel Limits | 3 Marks |
| **TC4** | MaxRequestBodySize value matches 10485760 bytes | 3 Marks |

**Total Score: 10 Marks**
