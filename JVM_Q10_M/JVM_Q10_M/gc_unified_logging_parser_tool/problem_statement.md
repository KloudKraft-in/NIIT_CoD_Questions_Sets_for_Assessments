# JVM Lab: GC unified logging parser tool

Duration : 60 Min.

## Scenario
Operations needs a command-line script to parse long JVM GC log files and extract indicators of GC pause durations exceeding SLAs.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Build a parser script that reads unified GC logs (-Xlog:gc*), filters pause times exceeding 150ms, calculates total GC pause overhead, and generates a JSON audit summary.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
1. Script parses standard unified GC log lines structure: 2.5 marks
2. Identify and extract pause times of individual collections: 2.5 marks
3. Filter pause duration occurrences exceeding 150ms limits: 2.5 marks
4. Calculate total cumulative GC time and frequency profiles: 2.5 marks
5. Identify GC pause triggers (Young/Full/System GC events): 2.5 marks
6. Isolate Eden/Tenured occupancy conversions information: 2.5 marks
7. Format parsing results into structured JSON summary format: 2.5 marks
8. Workspace diagnostics execution logs verification: 2.5 marks

**Total Score: 20 Marks**

## Important Notes
- This is a manually evaluated question.
- Ensure all logs and configurations are fully saved in your workspace folder before submitting.
