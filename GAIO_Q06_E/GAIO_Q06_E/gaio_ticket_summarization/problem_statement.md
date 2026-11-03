# GenAI Ops: AI Operational Support & Incident Ticket Summarization

Duration : 30 Min.

## Scenario
Use AI prompt output rules to summarize a lengthy multi-page incident support ticket. Extract incident severity, impacted microservices, and root cause.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/incident_summary.json`
**Input Resource File to Inspect**: `student_workspace/raw_incident_ticket.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `raw_incident_ticket.txt` in `student_workspace/`.
- Create or update `student_workspace/incident_summary.json` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `raw_incident_ticket.txt` inside `student_workspace/`.
3. Create or open `student_workspace/incident_summary.json` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | incident_summary.json exists | 3 Marks |
| **TC2** | Severity correctly extracted (P1/CRITICAL) | 4 Marks |
| **TC3** | Impacted service name ('payment-gateway') identified | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
