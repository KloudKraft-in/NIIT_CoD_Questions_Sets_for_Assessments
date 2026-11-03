# Observability Lab: Multi-Tool Telemetry Correlation & Incident Root Cause Analysis

Duration : 60 Min.

## Scenario
A major outage affects a distributed microservices platform. You must correlate metrics, logs, and traces across Datadog, Splunk, and Grafana.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Correlate metric anomalies with log stack traces and distributed trace spans to construct a Root Cause Analysis (RCA) report.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Tracing metric spikes in Grafana back to log exception bursts in Splunk: 5 marks
2. Correlating distributed trace IDs across multi-tier microservice calls: 5 marks
3. Isolating the primary root cause component versus cascading downstream failures: 5 marks
4. Documenting an end-to-end incident timeline with supporting telemetry evidence: 5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
