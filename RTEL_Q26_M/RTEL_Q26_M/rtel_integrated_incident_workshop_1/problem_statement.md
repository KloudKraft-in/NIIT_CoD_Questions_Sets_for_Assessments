# Observability Lab: Production Microservice Outage Triage & Incident Report

Duration : 90 Min.

## Scenario
A major e-commerce gateway experiences catastrophic response delays. You must investigate metrics, logs, and traces to author an RCA report.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Perform multi-tool incident triage across Datadog APM, Splunk logs, and Grafana metrics, then author a comprehensive incident post-mortem report.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Constructing a chronological timeline of outage milestones: 3 marks
2. Analyzing Grafana Golden Signal charts to pinpoint initial latency degradation: 3 marks
3. Executing Splunk SPL queries to isolate application exception stack traces: 3 marks
4. Inspecting Datadog flame graphs to identify the exact failing backend database call: 3 marks
5. Calculating total Error Budget consumed during the outage window: 2 marks
6. Formulating immediate operational remediation steps taken to restore service: 2 marks
7. Recommending architectural mitigations to prevent recurring failures: 2 marks
8. Structuring a formal Root Cause Analysis (RCA) report with supporting telemetry artifacts: 2 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
