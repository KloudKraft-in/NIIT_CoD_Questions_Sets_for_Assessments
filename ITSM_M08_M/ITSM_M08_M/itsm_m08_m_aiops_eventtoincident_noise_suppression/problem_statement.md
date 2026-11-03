# ITSM Lab: AIOps Event-to-Incident Noise Suppression, Correlation & Auto-Remediation Workflow

Duration : 90 Min.

## Scenario
A regional cloud datacenter network flap generates 2,500 raw monitoring alerts in 15 minutes, threatening to overwhelm the Service Desk. Configure an AIOps event management strategy: define noise suppression thresholds, create alert deduplication and correlation rules, cluster alerts into a single actionable Incident record, trigger an automated Ansible remediation runbook, and measure the resulting MTTA/MTTR delta.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Analyze high-volume raw alert streams and identify alert storm patterns.
- Define event filtering and deduplication rules to suppress alert noise by >80%.
- Correlate multi-source alerts into a single consolidated ServiceNow incident.
- Map the automated remediation trigger to execute an Ansible runbook.
- Verify service health post-automation and update incident work notes.
- Compare MTTR of automated remediation vs traditional L1.5/L2 human triage.
- Identify auto-remediation candidates across recurring incident profiles.
- Define guardrails and fallback escalation paths when auto-remediation fails.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Quantitative analysis of raw alert storm data and classification of noise versus actionable signals: 3 marks
2. Formulation of event filtering and deduplication policies achieving >80% noise reduction: 3 marks
3. Configuration of correlation rules binding disparate alerts to single parent CI incidents: 3 marks
4. Design of automated diagnostic and self-healing runbook execution workflows: 2 marks
5. Verification of automated remediation outcomes with audit trail logging in ServiceNow: 2 marks
6. Comparative mathematical calculation of MTTR and engineer effort savings through AIOps: 2 marks
7. Strategic identification of high-frequency incident profiles suitable for automation expansion: 3 marks
8. Establishment of safety guardrails, circuit breakers, and human escalation fallback mechanisms: 2 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
