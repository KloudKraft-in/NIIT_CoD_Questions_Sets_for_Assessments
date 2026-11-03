# GenAI Ops: Prompt Refinement & Iterative Optimization

Duration : 30 Min.

## Scenario
Iteratively improve a root cause analysis prompt across 3 revisions, increasing specificity, role clarity, and output constraints.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/iterations.json`
**Input Resource File to Inspect**: `student_workspace/base_rca_prompt.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `base_rca_prompt.txt` in `student_workspace/`.
- Create or update `student_workspace/iterations.json` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `base_rca_prompt.txt` inside `student_workspace/`.
3. Create or open `student_workspace/iterations.json` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | iterations.json contains 3 distinct iteration entries | 3 Marks |
| **TC2** | Iteration 3 includes explicit JSON output schema constraints | 4 Marks |
| **TC3** | Prompt text length increases monotonically across iterations | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
