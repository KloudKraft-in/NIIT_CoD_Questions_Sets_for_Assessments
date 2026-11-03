# Middleware Lab: Load Balancing and Session Sticky Settings

Duration : 90 Min.

## Scenario
A load balancer distributes requests across three web nodes. Users report losing session data intermittently.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure sticky session parameters on Nginx reverse proxy and setup cluster session persistence rules.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Configuring upstream server groups and server weights: 5 marks
2. Implementing ip_hash or sticky cookie configuration options: 5 marks
3. Setting up backend node health checks and failover intervals: 5 marks
4. Documenting Tomcat session replication architectures: 5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
