# JVM Lab: JVM Startup Heap Sizing

Duration : 30 Min.

## Scenario
A production Spring Boot service crashes under load because its memory boundaries are not defined. You need to configure appropriate startup parameters to enforce stability.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure JVM heap memory boundaries (-Xms and -Xmx to 512MB) and enable HeapDumpOnOutOfMemoryError in the JVM startup configuration file inside student_workspace.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Primary JVM heap sizing configurations (-Xms/-Xmx): 5 marks
2. OutOfMemory configuration setup and workspace scripts verification: 5 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
