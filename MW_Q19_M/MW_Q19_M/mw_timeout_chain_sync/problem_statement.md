# Middleware Lab: Timeout Chain Synchronization

Duration : 90 Min.

## Scenario
API calls timeout at Nginx (60s) before WebLogic App Server times out (120s), resulting in resource leaks.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Synchronize timeouts sequentially across reverse proxy, application server, and DB connection pool tiers.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Mapping current timeout configurations across all layers of request flow: 5 marks
2. Configuring proxy_read_timeout and proxy_connect_timeout in Nginx: 5 marks
3. Modifying connection timeouts on application servers and DB pools: 5 marks
4. Designing timeout cascade hierarchies (Gateway > Proxy > App > DB): 5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
