# Basic Code Analysis: ASP.NET Core Dependency Injection Lifetimes

Duration : 30 Min.

## Scenario
A C# API is registering services incorrectly, causing memory leaks due to transient scopes accessing DBContext. Set proper lifecycles.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/Program.cs`
**Input Resource File to Inspect**: `student_workspace/Program.cs`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Edit 'Program.cs' to change registration for 'IDbService' from AddTransient to AddScoped.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `Program.cs` inside `student_workspace/`.
3. Open `Program.cs` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Program.cs file exists | 3 Marks |
| **TC2** | IDbService registered as AddScoped | 4 Marks |
| **TC3** | Transient database configurations removed | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
