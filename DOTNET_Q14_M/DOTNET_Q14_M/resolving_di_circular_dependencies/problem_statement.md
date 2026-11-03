# .NET Lab: Resolving DI Circular Dependencies

Duration : 60 Min.

## Scenario
A circular dependency loop between three components ServiceA, ServiceB, and ServiceC blocks DI containers on startup.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Refactor Program.cs and breaking classes interfaces to resolve the circular loop.

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
| **TC3** | ServiceA registered under DI container | 3 Marks |
| **TC4** | ServiceB registered under DI container | 3 Marks |
| **TC5** | ServiceC registered under DI container | 3 Marks |
| **TC6** | Circular dependency between A, B, C is resolved | 3 Marks |
| **TC7** | Services compiled cleanly | 3 Marks |
| **TC8** | Interface dependencies introduced to abstract circular binds | 2 Marks |

**Total Score: 20 Marks**
