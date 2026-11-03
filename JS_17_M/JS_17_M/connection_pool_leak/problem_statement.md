# Java Lab: Connection Pool Leak Identification

Duration : 60 Min.

## Scenario
Configure HikariCP diagnostics properties inside `application.properties` to log connections that are not returned to the pool and simulate starvation.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Open `src/main/resources/application.properties`.
2. Configure the following database connection leak discovery options:
   - Enable connection leak logging detection threshold of 2 seconds (2000 ms):
     `spring.datasource.hikari.leak-detection-threshold=2000`
   - Set maximum wait time to get connection from the pool to 5 seconds (5000 ms):
     `spring.datasource.hikari.connection-timeout=5000`
3. Save the file.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | `application.properties` file exists | 10 Marks |
| **TC2   | `spring.datasource.hikari.leak-detection-threshold` is set exactly to 2000 | 10 Marks |
| **TC3   | `spring.datasource.hikari.connection-timeout` is set exactly to 5000 | 10 Marks |

**Total Score: 30 Marks**
