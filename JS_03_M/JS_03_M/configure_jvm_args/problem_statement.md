# Java Lab: Configure JVM Args for Containerised Workloads

Duration : 60 Min.

## Scenario
Configure JVM arguments in a startup script for a Java application running in a containerised environment. You are deploying a Spring Boot application (`app.jar`) into a Linux container. By default, the JVM might not optimally detect the container's memory constraints or use the best garbage collector. You have been provided with a `start.sh` script that currently just runs `java -jar app.jar`. You must update this script to include specific JVM flags to optimize memory and performance.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Edit the `start.sh` script.
- Add the flag `-XX:MaxRAMPercentage=75.0` to ensure the JVM uses 75% of the container's available RAM for the heap.
- Add the flag `-XX:+UseG1GC` to explicitly use the G1 Garbage Collector.
- Ensure the script still correctly executes the `app.jar` in the background (e.g., using `nohup` or `&`).
- Run the script and ensure the Java process remains active in the background.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives (e.g., `src/main/java/...`).
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands (like `mvn clean`), open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | `start.sh` contains the `-XX:MaxRAMPercentage=75.0` flag | 4 Marks |
| **TC2** | `start.sh` contains the `-XX:+UseG1GC` flag | 4 Marks |
| **TC3** | `start.sh` correctly executes the `.jar` file | 4 Marks |
| **TC4** | The Java process successfully starts and remains running | 4 Marks |
| **TC5** | The running Java process actively has the specified flags applied in memory | 4 Marks |

**Total Score: 20 Marks**
