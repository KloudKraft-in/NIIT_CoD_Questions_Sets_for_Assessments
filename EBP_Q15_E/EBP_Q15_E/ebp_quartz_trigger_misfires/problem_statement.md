# Enterprise Batch Lab: Resolving Quartz Trigger Misfires

Duration : 45 Min.

## Scenario
Under heavy JVM load, Quartz triggers misfire and skip critical report schedules. You need to configure misfire instructions.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure the Quartz properties file to define thread pools and misfire threshold settings.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Configuring thread pool size to prevent resource starvation: 3 marks
2. Setting org.quartz.jobStore.misfireThreshold values: 3 marks
3. Setting appropriate misfire instructions (e.g. Fire And Proceed): 2 marks
4. Customizing persistence rules for clustered environments: 2 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
