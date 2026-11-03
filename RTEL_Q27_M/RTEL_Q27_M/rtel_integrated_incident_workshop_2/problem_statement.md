# Observability Lab: Distributed DB Deadlock & Memory Leak Multi-Tool RCA

Duration : 90 Min.

## Scenario
A financial settlement service encounters thread pool exhaustion and database deadlock failures under peak load.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Correlate JVM heap memory metrics, database lock logs, and distributed trace spans to isolate memory leaks and deadlocks.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Correlating JVM garbage collection pauses with application response latencies: 3 marks
2. Analyzing database lock logs in Splunk to identify deadlocking SQL statements: 3 marks
3. Tracing blocked HTTP executor threads using Dynatrace PurePath: 3 marks
4. Isolating unclosed database connection pools causing memory leaks: 3 marks
5. Evaluating connection pool configuration parameters and recommending optimal limits: 3 marks
6. Formulating database index and transaction isolation level adjustments: 2 marks
7. Documenting a step-by-step incident post-mortem report with evidence charts: 3 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
