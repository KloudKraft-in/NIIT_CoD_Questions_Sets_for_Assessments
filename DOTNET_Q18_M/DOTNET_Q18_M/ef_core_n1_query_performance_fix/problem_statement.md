# .NET Lab: EF Core N1 Query Performance Fix

Duration : 60 Min.

## Scenario
The Sales query performance degraded. A database trace log indicates an N+1 query loop fetching SalesOrderLines sequentially.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Refactor OrderRepository.cs to use eager loading Include and read-only AsNoTracking optimization.

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
| **TC2** | File OrderRepository.cs exists in workspace | 3 Marks |
| **TC3** | Eager loading Include used to query OrderLines | 3 Marks |
| **TC4** | Eager loading reduces database roundtrips to a single query | 3 Marks |
| **TC5** | AsNoTracking optimization applied for read-only query | 3 Marks |
| **TC6** | Repository compiles cleanly | 2 Marks |
| **TC7** | Eager loading logic correctly projects columns | 2 Marks |
| **TC8** | OrderLines collection returned matching loop counts | 2 Marks |
| **TC9** | No redundant loops remain inside the query method | 2 Marks |

**Total Score: 20 Marks**
