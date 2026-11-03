# ITSM Lab: Storage Volume Near-Capacity Escalation - iRUN Escalation Matrix & Context Handoff

Duration : 30 Min.

## Scenario
An incident assigned to the Service Desk reveals that a production SAN storage volume hosting database transactions is at 94% capacity. Storage engineering is outside the Service Desk's remit. Rather than dumping the ticket without data ('throwing it over the wall'), the analyst must apply the iRUN Functional Escalation Matrix, assemble a compliant context handoff package (diagnostic command outputs, growth rate, current allocation, business risk), and transfer ownership cleanly to avoid bounce-back.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Apply the iRUN escalation matrix criteria to determine the correct target resolver group.
- Compile mandatory diagnostic context including storage volume mount, filesystem utilization, and process consumers.
- Author a structured escalation handoff note preventing ticket bounce-back and SLA slippage.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Application of functional escalation matrix rules to identify the exact target engineering domain: 4 marks
2. Assembly of required technical diagnostic context and capacity utilization metrics: 3 marks
3. Drafting of compliant escalation transfer summary adhering to zero-bounce standards: 3 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
