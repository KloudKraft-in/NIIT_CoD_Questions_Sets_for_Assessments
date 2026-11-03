# Middleware Lab: Log Correlation and Multi-Hop Tracing

Duration : 90 Min.

## Scenario
Tracing errors in distributed environments is difficult without standard tracking keys across microservice boundaries.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure request tracing headers at the gateway and map them through application logs using correlation variables.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Configuring unique Request ID header generation in Nginx (X-Request-ID): 7 marks
2. Mapping logging frameworks (Logback/MDC) to capture and output correlation IDs: 6 marks
3. Tracing request hops across middleware components and queues: 6 marks
4. Creating a step-by-step transaction analysis report for failed workflows: 6 marks

**Total Score: 25 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
