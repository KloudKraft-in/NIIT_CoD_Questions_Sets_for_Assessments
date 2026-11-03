# Java Lab: Common Java Log Signatures Analysis

Duration : 60 Min.

## Scenario
Filter and extract signature error flags from system logs. Parse a Java application log file `server.log` to identify and count standard exceptions.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Examine `server.log`.
2. Write a script `analyze.sh` or program to output the count of these three exceptions to `log_summary.json`:
   - `NullPointerException`
   - `ClassNotFoundException`
   - `BeanCreationException`
3. Save the results as a JSON structure:
   `{"NullPointerException": X, "ClassNotFoundException": Y, "BeanCreationException": Z}`

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `log_summary.json` exists and is valid JSON | 2 Marks |
| **TC2**   | Count of `NullPointerException` is correct | 2 Marks |
| **TC3**   | Count of `ClassNotFoundException` is correct | 2 Marks |
| **TC4**   | Count of `BeanCreationException` is correct | 2 Marks |
| **TC5**   | All exception frequencies calculated accurately | 2 Marks |

**Total Score: 10 Marks**
