# .NET Lab: Kestrel HTTP2 Endpoint Configuration

Duration : 30 Min.

## Scenario
To support high-throughput HTTP/2 multiplexing, you must explicitly enable HTTP/2 protocols in Kestrel configuration.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Modify appsettings.json to add a 'Http2' protocol configuration on port 5001.

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
| **TC2** | File appsettings.json exists and is valid JSON | 5 Marks |
| **TC3** | Endpoint configuration for Kestrel is set on port 5001 | 5 Marks |
| **TC4** | Protocols list includes Http2 or Http1AndHttp2 | 5 Marks |
| **TC5** | Kestrel configuration contains valid default SSL certificate references | 5 Marks |

**Total Score: 20 Marks**
