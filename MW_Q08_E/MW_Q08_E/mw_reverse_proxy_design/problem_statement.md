# Middleware Lab: Reverse Proxy Routing Design

Duration : 30 Min.

## Scenario
To secure backend applications, Nginx must act as a reverse proxy, routing incoming client traffic based on request paths.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure location blocks in nginx.conf using proxy_pass while preserving client headers.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Configuring location directives and target proxy_pass URLs: 3 marks
2. Preserving client headers (Host, X-Real-IP, X-Forwarded-For): 3 marks
3. Configuring client body size and buffer limits: 4 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
