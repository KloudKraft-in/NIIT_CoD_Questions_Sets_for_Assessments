# .NET Lab: CLR Thread Pool Starvation

Duration : 120 Min.

## Scenario
A Web API application undergoes severe latency spikes under load. Thread dump diagnostics indicate Thread Pool starvation.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Investigate sync-over-async blocking calls in data repositories, refactor synchronous operations to async/await patterns, and document performance improvements.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Thread pool starvation scenario reproduction logs: 2.5 marks
2. Sync-over-async blocking methods profiling metrics: 2.5 marks
3. Asynchronous database calls refactoring code implementation: 2.5 marks
4. Thread pool worker count metrics comparison reports: 2.5 marks
5. CLR diagnostics tracing file captures validation: 2.5 marks
6. Starvation prevention configuration tuning parameters: 2.5 marks
7. Application response latency SLA checks validation: 2.5 marks
8. Incident RCA report and escalation post-mortem document: 2.5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
