# Middleware Lab: Tomcat Executor Thread Pool Tuning

Duration : 90 Min.

## Scenario
A thread dump of a slow application server reveals that all HTTP worker threads are in a blocked state.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Tune the application server executor pool limits to maximize request concurrency and throughput.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Configuring the shared Executor thread block in Tomcat server.xml: 5 marks
2. Tuning maxThreads and minSpareThreads values to optimize throughput: 5 marks
3. Configuring connection acceptCount queue limits: 5 marks
4. Analyzing thread states (RUNNABLE, WAITING) to diagnose bottlenecks: 5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
