# Java Lab: Reading Java Startup Banner & Logs

Duration : 60 Min.

## Scenario
Analyze a standard Spring Boot console startup log file (`startup.log`) to parse dependency details, JVM version, and system diagnostics information, then write the extracted values into a structured report (`report.json`).

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Examine the `startup.log` file provided in your workspace.
2. Edit or create a script `parse_log.py` (or write a quick utility/run a shell pipeline) that parses the log file.
3. Extract the following information and output it to `report.json` in the `student_workspace` directory:
   - `java_version`: The JVM version found in the startup logs.
   - `spring_boot_version`: The version of Spring Boot printed in the banner or startup line.
   - `warn_count`: The total count of log lines starting with or containing `WARN` or `WARNING`.
4. Ensure the output file `report.json` is formatted as a valid JSON object.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `report.json` exists and is valid JSON | 3 Marks |
| **TC2**   | Extracted Java version and Spring Boot version are correct | 4 Marks |
| **TC3**   | Count of warnings (`warn_count`) is correct | 3 Marks |

**Total Score: 10 Marks**
