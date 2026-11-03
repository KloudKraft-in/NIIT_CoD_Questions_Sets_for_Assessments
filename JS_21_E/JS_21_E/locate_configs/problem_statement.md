# Java Lab: Locate Custom Configs on Classpath

Duration : 60 Min.

## Scenario
Create and locate a custom application properties configuration on the Java Classpath resources.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Create a directory structure `src/main/resources/` if it does not exist.
2. In that directory, create a file named `additional-config.properties`.
3. Add the custom configuration line:
   `app.custom.value=42`
4. Save the file.

## Verification
Run the verification script to receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | `additional-config.properties` exists on classpath | 3 Marks |
| **TC2   | custom value property defined | 3 Marks |
| **TC3   | `app.custom.value` set exactly to 42 | 4 Marks |

**Total Score: 10 Marks**
