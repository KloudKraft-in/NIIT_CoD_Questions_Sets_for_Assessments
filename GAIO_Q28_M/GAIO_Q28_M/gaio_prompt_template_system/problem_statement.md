# GenAI Ops: Reusable Operational Prompt Template System

Duration : 90 Min.

## Scenario
Build an operational prompt template manager ('template_manager.py') that organizes reusable templates across 8 operational categories with variable substitution.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/template_manager.py`
**Input Resource File to Inspect**: `student_workspace/op_categories_spec.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `generated_script.py` in `student_workspace/`.
- Create or update `student_workspace/template_manager.py` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `generated_script.py` inside `student_workspace/`.
3. Create or open `student_workspace/template_manager.py` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | template_manager.py is syntax-valid Python | 4 Marks |
| **TC2** | Supports 8 operational categories (Incident, Log, RCA, Change, etc.) | 4 Marks |
| **TC3** | Implements variable substitution engine for {placeholders} | 4 Marks |
| **TC4** | Outputs valid template_library.json | 4 Marks |
| **TC5** | Validates template variable completeness | 3 Marks |
| **TC6** | Prevents duplicate template names | 2 Marks |
| **TC7** | Provides template search by category function | 2 Marks |
| **TC8** | Exports default system prompt configuration | 2 Marks |

**Total Score: 25 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
