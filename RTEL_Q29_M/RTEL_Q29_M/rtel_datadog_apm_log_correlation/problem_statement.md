# Observability Lab: Datadog Multi-Tier Latency Spike Audit & Monitor Setup

Duration : 90 Min.

## Scenario
A cloud-native microservices cluster suffers cascading latency spikes. You must use Datadog APM, Log Rehydration, and Monitors to resolve it.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Audit multi-tier request flows in Datadog APM, correlate log streams with trace IDs, configure composite monitors, and tune alert hygiene.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Tracing cascading latency spikes across microservices using Datadog APM: 3 marks
2. Correlating trace IDs with rehydrated log archives to extract exception payloads: 3 marks
3. Configuring Datadog composite monitors combining metric and log conditions: 3 marks
4. Tuning alert thresholds using dynamic anomaly detection to eliminate false alarms: 3 marks
5. Setting up automated PagerDuty integration and runbook links: 3 marks
6. Developing a telemetry cost optimization plan by dropping low-value log indexes: 2 marks
7. Authoring an executive incident report detailing root cause and action items: 3 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
