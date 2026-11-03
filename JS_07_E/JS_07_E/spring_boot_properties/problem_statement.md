# Java Lab: Spring Boot Externalized Configuration Override

Duration : 60 Min.

## Scenario
Override Spring Boot configuration parameters at runtime using an external configuration file `application-ext.properties`.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate the configuration directory. Create `config/application-ext.properties` if it does not exist.
2. Add the following override properties:
   - `spring.profiles.active=staging`
   - `database.connection.timeout=5000`
3. Save the file.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `config/application-ext.properties` exists | 3 Marks |
| **TC2**   | Profile override set to `staging` | 4 Marks |
| **TC3**   | Timeout override set to `5000` | 3 Marks |

**Total Score: 10 Marks**
