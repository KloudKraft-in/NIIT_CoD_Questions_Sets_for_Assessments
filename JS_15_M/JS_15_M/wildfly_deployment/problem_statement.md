# Java Lab: JBoss / WildFly Standalone App Server Deployment

Duration : 60 Min.

## Scenario
Configure standalone server listener port bindings inside WildFly configuration directories.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `configuration/standalone.xml`.
2. Configure the HTTP socket binding port setting to offset default port listening parameters from `8080` to `8082`:
   `<socket-binding name="http" port="8082"/>`

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | standalone WildFly mode check | 3 Marks |
| **TC2   | custom port offset set to 2 | 3 Marks |
| **TC3   | standalone.xml XML matches | 3 Marks |
| **TC4   | HTTP port bound to 8082 | 3 Marks |
| **TC5   | deployment.properties exists | 3 Marks |
| **TC6   | Active deployment scanner properties | 3 Marks |
| **TC7   | Standalone deployment scanner configured | 3 Marks |
| **TC8   | App deployment listener running | 4 Marks |

**Total Score: 25 Marks**
