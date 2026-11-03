# GenAI Ops: Constrained JSON Incident Report Generator

Duration : 45 Min.

## Scenario
Design a system prompt instruction that strictly forces an LLM to output valid JSON conforming to an incident report JSON schema.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/system_prompt_spec.json`
**Input Resource File to Inspect**: `student_workspace/json_schema_spec.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `json_schema_spec.txt` in `student_workspace/`.
- Create or update `student_workspace/system_prompt_spec.json` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `json_schema_spec.txt` inside `student_workspace/`.
3. Create or open `student_workspace/system_prompt_spec.json` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | system_prompt_spec.json exists | 3 Marks |
| **TC2** | Requires root-level JSON object wrapper | 3 Marks |
| **TC3** | Mandatory keys (incident_id, severity, rca) specified | 2 Marks |
| **TC4** | Prohibits markdown code block wrappers | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
