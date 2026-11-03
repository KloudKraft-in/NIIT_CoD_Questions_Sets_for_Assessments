# Middleware Lab: SSL/TLS Certificate Trust Chain Diagnostics

Duration : 45 Min.

## Scenario
Clients connecting to a secure Tomcat container receive SSL validation errors due to incomplete trust chains.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Analyze SSL logs, configure certificate bundles, and import trusted root CAs into truststores.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Verifying certificate expiration dates and domain name matches: 3 marks
2. Configuring intermediate certificate bundles in server config: 3 marks
3. Importing missing root certificates into Java Truststores: 4 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
