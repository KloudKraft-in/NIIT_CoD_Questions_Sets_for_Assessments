# .NET Lab: Diagnosing CPU Spike with dotnet-dump

Duration : 60 Min.

## Scenario
A production ASP.NET Core service experiences a 100% CPU lock spike. A process memory dump was captured using dotnet-dump.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Analyze the thread stacks, identify lock address and contention thread ID, and document details in diagnostics.md.

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
| **TC2** | Diagnostics report diagnostics.md exists | 3 Marks |
| **TC3** | Report identifies dotnet-dump analysis command used | 3 Marks |
| **TC4** | Report locates the exact thread ID triggering CPU spike | 3 Marks |
| **TC5** | Report isolates lock address where threads are blocked | 3 Marks |
| **TC6** | Report identifies class method name blocking thread execution | 3 Marks |
| **TC7** | Report lists correct thread state (BLOCKED / WAITING) | 3 Marks |
| **TC8** | Recommendation section specifies code patch utilizing async locks | 2 Marks |

**Total Score: 20 Marks**
