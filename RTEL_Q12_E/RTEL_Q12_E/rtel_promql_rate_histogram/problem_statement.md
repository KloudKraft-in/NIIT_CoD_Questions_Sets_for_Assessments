# Observability Lab: PromQL Instant vs Range Vector Calculations

Duration : 30 Min.

## Scenario
A Kubernetes cluster administrator needs to calculate HTTP request rates and 99th percentile response latencies using Prometheus.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Write PromQL queries utilizing rate(), increase(), histogram_quantile(), and label matching functions.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Constructing PromQL queries using rate() and increase() range vector functions: 4 marks
2. Calculating p99 latency percentiles using histogram_quantile(): 3 marks
3. Applying label matching and aggregation operators (by, without) to filter metrics: 3 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
