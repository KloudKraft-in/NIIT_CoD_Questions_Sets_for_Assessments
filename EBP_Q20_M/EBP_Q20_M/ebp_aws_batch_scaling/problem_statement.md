# Enterprise Batch Lab: Scaling AWS Batch Compute Environments

Duration : 90 Min.

## Scenario
Under heavy workload bursts, AWS Batch compute environments fail to scale out quickly enough, leading to container allocation timeouts.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Configure allocation strategies, instance type whitelists, and launch templates for optimal scaling.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Configuring Auto Scaling launch template settings: 3 marks
2. Whitelisting instance type families for compute workloads: 3 marks
3. Configuring allocation strategy parameters (e.g. BEST_FIT_PROGRESSIVE): 3 marks
4. Setting maximum and minimum vCPU threshold levels: 3 marks
5. Customizing security groups and IAM instance profile bindings: 2 marks
6. Creating CloudWatch alarms for scale-out bottlenecks: 2 marks
7. Documenting spot-instance fallback strategies: 2 marks
8. Optimizing container startup configurations: 2 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
