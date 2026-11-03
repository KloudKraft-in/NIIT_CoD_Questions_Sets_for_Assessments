# Observability Lab: Advanced Splunk SPL Timechart & Transaction Auditing

Duration : 60 Min.

## Scenario
An investigation requires analyzing error rate trends over time and tracking multi-step user checkout workflows in Splunk.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Write advanced SPL queries utilizing timechart, span, transaction, maxspan, and lookup commands to identify workflow drop-offs.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Constructing timechart queries with custom span intervals to visualize error spikes: 8 marks
2. Grouping user session events using the transaction command with maxspan limits: 8 marks
3. Enriching log event fields using Splunk CSV lookup tables: 7 marks
4. Calculating transaction completion percentages and drop-off rates: 7 marks

**Total Score: 30 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
