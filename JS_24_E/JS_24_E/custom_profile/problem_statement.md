# Java Lab: Custom Profile Activation

Duration : 60 Min.

## Scenario
Activate a custom configuration profile `secure-db` to enable database encryption properties.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `application.properties`.
2. Configure the active profile to load custom configuration options:
   `spring.profiles.active=secure-db`
3. Save the file.

## Verification
Run the verification script to receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | `application.properties` exists | 3 Marks |
| **TC2   | `spring.profiles.active` property defined | 3 Marks |
| **TC3   | `spring.profiles.active` set to secure-db | 4 Marks |

**Total Score: 10 Marks**
