# GenAI Ops: Integrated Real-World AI Ops Incident Resolution Workshop

Duration : 90 Min.

## Scenario
A major production incident occurred. Run an integrated AI Ops resolution workflow: analyze ticket, audit AI-suggested commands, sanitize logs, apply CRISP prompts, and generate RCA.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/integrated_rca_workshop.json`
**Input Resource File to Inspect**: `student_workspace/capstone_incident_data.txt`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `capstone_incident_data.txt` in `student_workspace/`.
- Create or update `student_workspace/integrated_rca_workshop.json` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `incident_bundle.json` inside `student_workspace/`.
3. Create or open `student_workspace/integrated_rca_workshop.json` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | integrated_rca_workshop.json exists and is valid JSON | 4 Marks |
| **TC2** | Incident root cause correctly mapped to database deadlock | 4 Marks |
| **TC3** | AI-suggested command audit completed (dangerous commands flagged) | 4 Marks |
| **TC4** | Log PII and API keys sanitized | 4 Marks |
| **TC5** | CRISP framework prompt applied for ticket response | 3 Marks |
| **TC6** | Remediation verification checklist provided | 2 Marks |
| **TC7** | Post-mortem timeline entries sequential | 2 Marks |
| **TC8** | Long-term AI Ops governance recommendation included | 2 Marks |

**Total Score: 25 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
