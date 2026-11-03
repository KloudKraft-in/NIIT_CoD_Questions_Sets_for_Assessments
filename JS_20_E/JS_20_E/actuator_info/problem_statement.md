# Java Lab: Spring Actuator Info Configuration

Duration : 60 Min.

## Scenario
Expose the basic `/actuator/info` endpoint for application diagnostics.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `application.properties`.
2. Configure the endpoints web exposure properties:
   `management.endpoints.web.exposure.include=info`
3. Save the file.

## Verification
Run the verification script to receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | `application.properties` exists | 3 Marks |
| **TC2   | web exposure include property defined | 3 Marks |
| **TC3   | info endpoint is correctly exposed | 4 Marks |

**Total Score: 10 Marks**
