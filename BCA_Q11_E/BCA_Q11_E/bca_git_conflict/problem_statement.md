# Basic Code Analysis: Resolving Merge Conflicts

Duration : 30 Min.

## Scenario
You run a git merge command and encounter conflict markers inside the repository. Inspect the workspace, identify the conflicting branch name and the file containing conflict markers, and document them in `solution.json`.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/auth.js`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Run `python setup_git.py` (or `python run.py`) to initialize/verify the Git conflict scenario if needed.
- Create/update `solution.json` with the following format:
```json
{
  "conflicting_branch": "feature/login",
  "conflict_file": "auth.js"
}
```

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Inspect `auth.js` and Git details inside `student_workspace/`.
3. Create or update `solution.json` inside `student_workspace/` with the identified branch and file.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | solution.json exists in student_workspace/ | 3 Marks |
| **TC2** | Conflicting branch name ('feature/login') identified | 4 Marks |
| **TC3** | Conflict marker file ('auth.js') correctly identified | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
