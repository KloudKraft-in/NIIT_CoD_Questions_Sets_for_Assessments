# .NET Lab: EF Core DbContext Connection Pooling

Duration : 60 Min.

## Scenario
To optimize connection handling under high concurrent request spikes, you need to set up DbContext pooling rules.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Modify Program.cs to use DbContext Connection Pooling for SalesDbContext instead of standard transient Context registration.

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
| **TC2** | Program.cs exists in workspace | 3 Marks |
| **TC3** | DbContext class 'SalesDbContext' defined | 3 Marks |
| **TC4** | DbContext pooling configured using AddDbContextPool method | 3 Marks |
| **TC5** | Connection string retrieval configured | 3 Marks |
| **TC6** | Pool size parameter configured explicitly | 3 Marks |
| **TC7** | Code compiles cleanly | 3 Marks |
| **TC8** | No redundant AddDbContext registration remains | 2 Marks |

**Total Score: 20 Marks**
