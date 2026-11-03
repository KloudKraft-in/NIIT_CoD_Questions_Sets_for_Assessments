# Observability Lab: Loki LogQL Querying & JSON Parser Filtering

Duration : 30 Min.

## Scenario
An SRE team uses Grafana Loki for log aggregation. You must write LogQL queries to parse structured JSON log lines and filter error spikes.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Write LogQL log stream selectors, line filters, JSON parser stages, and count_over_time rate calculations.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Formulating LogQL stream selectors and regex line filters: 3 marks
2. Parsing JSON log payloads and extracting dynamic label fields: 3 marks
3. Calculating error log message rates using count_over_time() and rate(): 4 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
