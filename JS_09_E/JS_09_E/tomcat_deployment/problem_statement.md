# Java Lab: Tomcat Standalone App Server Deployment

Duration : 60 Min.

## Scenario
Configure credentials and roles on a classical Apache Tomcat application server to allow administrators to deploy applications via the Manager UI.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate the Apache Tomcat configuration file `conf/tomcat-users.xml`.
2. Configure a new role `manager-gui`.
3. Add a user named `admin` with password `secrettomcat` and assign them the `manager-gui` role.
4. Save the file.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | `conf/tomcat-users.xml` file exists and is valid XML | 2 Marks |
| **TC2**   | A role named `manager-gui` is defined | 2 Marks |
| **TC3**   | A user named `admin` is declared | 2 Marks |
| **TC4**   | User `admin` has password `secrettomcat` | 2 Marks |
| **TC5**   | User `admin` is assigned the `manager-gui` role | 2 Marks |

**Total Score: 10 Marks**
