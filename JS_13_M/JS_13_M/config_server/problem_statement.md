# Java Lab: Spring Cloud Config Server Integration

Duration : 60 Min.

## Scenario
Configure a centralized config client to fetch property structures from a Git-backed Config Server.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `src/main/resources/bootstrap.yml`.
2. Configure config client properties to point to config server URL `http://localhost:8888` and fetch application overrides:
   `spring.cloud.config.uri=http://localhost:8888`
   `spring.cloud.config.name=ops-app`

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | config client settings configured | 3 Marks |
| **TC2   | config server URI mapped | 3 Marks |
| **TC3   | spring.cloud.config.label is master/main | 3 Marks |
| **TC4   | config profile set | 3 Marks |
| **TC5   | Config bootstrap syntax valid | 3 Marks |
| **TC6   | Config server loaded | 3 Marks |
| **TC7   | Central property repo active | 3 Marks |
| **TC8   | Dynamic configs active | 4 Marks |

**Total Score: 25 Marks**
