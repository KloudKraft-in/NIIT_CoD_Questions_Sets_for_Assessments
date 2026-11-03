# ITSM Lab: SLA Dashboard Reconciliation - MTTA, MTTR & Breach Metric Calculation

Duration : 30 Min.

## Scenario
A weekly SLA executive report flags a breach on a critical P2 incident (target 30-minute response, 4-hour resolution). The assigned engineering lead disputes the breach, asserting that the team began immediate triage. The analyst must inspect six raw system timestamps (Logged, Assigned, Acknowledged, First Work Note, Restored, Closed), calculate exact MTTA and MTTR, audit whether pause states (On Hold - Awaiting Vendor) were valid, and determine actual SLA compliance.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Extract and compute MTTA and MTTR directly from raw ISO timestamps.
- Audit ticket timeline against SLA/OLA stop-the-clock conditions (On Hold awaiting customer/vendor).
- Reconcile reported SLA breach status versus actual active engineering time and formulate recommendations.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Accurate mathematical calculation of MTTA and MTTR from raw timestamp data: 4 marks
2. Validation of SLA clock state transitions and pause justification analysis: 3 marks
3. Determination of genuine SLA breach status and process improvement recommendations: 3 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
