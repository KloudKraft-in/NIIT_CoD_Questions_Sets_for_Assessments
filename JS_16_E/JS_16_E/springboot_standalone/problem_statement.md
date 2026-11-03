# Java Lab: Spring Boot Standalone Application Execution

Duration : 60 Min.

## Scenario
Configure a standalone Spring Boot application build setting to enable compiler target version 17 and pack it into a runnable JAR file.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `pom.xml`.
2. Configure the compiler properties to target Java 17:
   `<maven.compiler.source>17</maven.compiler.source>`
   `<maven.compiler.target>17</maven.compiler.target>`
3. Set the packaging type to JAR:
   `<packaging>jar</packaging>`
4. Save the file.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | `pom.xml` exists | 3 Marks |
| **TC2   | Java compilation properties set to 17 | 3 Marks |
| **TC3   | Packaging type set to JAR | 4 Marks |

**Total Score: 10 Marks**
