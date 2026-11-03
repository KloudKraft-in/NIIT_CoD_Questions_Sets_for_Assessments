# GenAI Ops: Multi-Step Sequential AI Workflows

Duration : 60 Min.

## Scenario
Build an automated Python workflow ('ai_workflow.py') that chains 3 sequential operational steps: Ticket Parsing -> Log Correlation -> RCA Report Generation.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/ai_workflow.py`
**Input Resource File to Inspect**: `student_workspace/incident_lifecycle_input.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `incident_lifecycle_input.txt` in `student_workspace/`.
- Create or update `student_workspace/ai_workflow.py` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `incident_lifecycle_input.txt` inside `student_workspace/`.
3. Create or open `student_workspace/ai_workflow.py` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | ai_workflow.py is syntax-valid Python | 5 Marks |
| **TC2** | Step 1 parses incident ticket payload | 5 Marks |
| **TC3** | Step 2 correlates log trace IDs | 5 Marks |
| **TC4** | Outputs structured final_rca_report.json file | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
