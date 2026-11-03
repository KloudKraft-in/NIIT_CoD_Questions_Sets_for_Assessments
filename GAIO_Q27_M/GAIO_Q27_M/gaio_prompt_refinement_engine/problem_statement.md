# GenAI Ops: Iterative Prompt Refinement Engine

Duration : 90 Min.

## Scenario
Develop a Python script ('refine_prompt.py') that evaluates 3 revisions of a prompt, calculates a quality metric per iteration, and enforces monotonic improvement.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/refine_prompt.py`
**Input Resource File to Inspect**: `student_workspace/prompt_revisions.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `prompt_revisions.txt` in `student_workspace/`.
- Create or update `student_workspace/refine_prompt.py` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `secops_payload.json` inside `student_workspace/`.
3. Create or open `student_workspace/refine_prompt.py` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | refine_prompt.py is syntax-valid Python | 3 Marks |
| **TC2** | Evaluates prompt specificity, role assignment, and output constraints | 3 Marks |
| **TC3** | Calculates quality score per iteration | 3 Marks |
| **TC4** | Enforces non-decreasing score constraint across iterations | 3 Marks |
| **TC5** | Writes refinement_summary.json | 2 Marks |
| **TC6** | Identifies best performing prompt iteration | 2 Marks |
| **TC7** | Logs delta improvement score | 2 Marks |
| **TC8** | Handles single-iteration fallback gracefully | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
