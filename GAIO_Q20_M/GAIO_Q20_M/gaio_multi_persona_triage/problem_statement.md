# GenAI Ops: Multi-Persona Incident Triage Prompting

Duration : 60 Min.

## Scenario
Construct a multi-persona prompt chain that simulates a collaborative incident triage between a Database Administrator and a Network SRE.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/multi_persona_config.json`
**Input Resource File to Inspect**: `student_workspace/database_lock_incident.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `database_lock_incident.txt` in `student_workspace/`.
- Create or update `student_workspace/multi_persona_config.json` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `database_lock_incident.txt` inside `student_workspace/`.
3. Create or open `student_workspace/multi_persona_config.json` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | multi_persona_config.json exists | 5 Marks |
| **TC2** | DBA persona focuses on locks and connection pools | 5 Marks |
| **TC3** | Network SRE persona focuses on latency and packet loss | 5 Marks |
| **TC4** | Consolidated RCA synthesis section defined | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
