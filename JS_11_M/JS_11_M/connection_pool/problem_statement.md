# Java Lab: Connection Pool Sizing and Saturated Latency

Duration : 60 Min.

## Scenario
Optimize HikariCP database connection pooling parameters inside `application.properties` to ensure maximum concurrency and prevent request timeouts.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Open `src/main/resources/application.properties`.
2. Configure the following pool limits:
   - `spring.datasource.hikari.maximum-pool-size=50`
   - `spring.datasource.hikari.connection-timeout=15000`
   - `spring.datasource.hikari.minimum-idle=10`
   - `spring.datasource.hikari.idle-timeout=600000`

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | maximum-pool-size set to 50 | 2 Marks |
| **TC2   | connection-timeout set to 15000 | 2 Marks |
| **TC3   | minimum-idle set to 10 | 2 Marks |
| **TC4   | idle-timeout set to 600000 | 2 Marks |
| **TC5   | Properties syntax valid | 3 Marks |
| **TC6   | Active connection settings loaded | 3 Marks |
| **TC7   | Starvation timeout limit active | 3 Marks |
| **TC8   | Min-idle background capacity active | 3 Marks |

**Total Score: 20 Marks**
