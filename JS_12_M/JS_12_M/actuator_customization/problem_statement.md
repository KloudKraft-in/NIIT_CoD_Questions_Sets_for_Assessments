# Java Lab: Spring Actuator Custom Endpoint & Log Level Security

Duration : 60 Min.

## Scenario
Add custom indicators and lock down Spring Actuator endpoints to enforce secure diagnostic visibility.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Edit `src/main/resources/application.properties`.
2. Expose the actuator endpoints `health`, `info`, and `loggers` using `management.endpoints.web.exposure.include=health,info,loggers`.
3. Force endpoint security role checks by declaring `management.endpoint.health.show-details=always`.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | health endpoint exposed | 2 Marks |
| **TC2   | info endpoint exposed | 2 Marks |
| **TC3   | show-details set to always | 2 Marks |
| **TC4   | loggers endpoint exposed | 2 Marks |
| **TC5   | Properties syntax valid | 3 Marks |
| **TC6   | Active connection settings loaded | 3 Marks |
| **TC7   | Endpoint security limits active | 3 Marks |
| **TC8   | Detailed health status metrics active | 3 Marks |

**Total Score: 20 Marks**
