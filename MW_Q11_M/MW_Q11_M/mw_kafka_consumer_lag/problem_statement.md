# Middleware Lab: Resolving Kafka Consumer Lag & Rebalances

Duration : 60 Min.

## Scenario
A Kafka consumer group frequently triggers rebalance storms under spike loads, causing processing lag to rise.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Analyze lag statistics, modify consumer poll properties, and optimize partition processing strategies.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Querying Kafka consumer group lag statistics: 5 marks
2. Configuring max.poll.interval.ms and session.timeout.ms parameter overrides: 5 marks
3. Analyzing rebalance triggers and implementing graceful shutdown hooks: 5 marks
4. Optimizing partition distribution mappings for parallel consumers: 5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
