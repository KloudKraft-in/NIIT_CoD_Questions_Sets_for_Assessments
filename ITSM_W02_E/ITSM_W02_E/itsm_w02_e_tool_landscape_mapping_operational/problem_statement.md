# ITSM Lab: Tool Landscape Mapping & Operational Investigation Order - ITSM vs Observability vs Automation

Duration : 60 Min.

## Scenario
During an operational triage drill, a support engineer must determine the appropriate enterprise tools (Datadog, ServiceNow, Rundeck, Confluence) to use across eight operational scenarios. You must classify each task into the correct tooling category, establish the canonical operational investigation order (why Observability precedes ITSM logging), and articulate how tools integrate during active incident handling.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Map 8 operational scenarios to their respective tool categories (ITSM, Observability, Automation, Knowledge Management).
- Document the correct operational investigation sequence and explain why Observability is the primary diagnostic source of truth.
- Design a cross-tool workflow showing how metric anomalies trigger incidents, execute automated runbooks, and update knowledge bases.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Correct classification of 8 operational activities across the four core enterprise tooling domains: 4 marks
2. Detailed technical justification of the diagnostic investigation sequence (Observability first, ITSM system of record): 3 marks
3. Specification of bidirectional synchronization between automated monitoring alerts and ServiceNow incident records: 3 marks

**Total Score: 10 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
