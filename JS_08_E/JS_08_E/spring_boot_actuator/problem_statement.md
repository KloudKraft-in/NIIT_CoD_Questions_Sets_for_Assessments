# Java Lab: Basic Spring Boot Actuator Health Check

Duration : 60 Min.

## Scenario
Add basic monitoring to a Spring Boot app by exposing Web Actuator endpoints.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `src/main/resources/application.properties`.
2. Add property:
   `management.endpoints.web.exposure.include=health`
3. Save the file.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `application.properties` updated successfully | 3 Marks |
| **TC2**   | Actuator health exposure configuration declared | 4 Marks |
| **TC3**   | Health endpoint enabled correctly | 3 Marks |

**Total Score: 10 Marks**
