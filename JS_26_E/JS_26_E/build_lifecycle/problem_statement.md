# Java Lab: Maven Source File Encoding

Duration : 60 Min.

## Scenario
Configure the default source file build encoding property inside `pom.xml` to prevent compile warnings in cross-platform builds.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `pom.xml`.
2. Configure the source encoding property under properties section:
   `<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>`
3. Save the file.

## Verification
Run the verification script to receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | `pom.xml` exists | 3 Marks |
| **TC2   | `<project.build.sourceEncoding>` property is defined | 3 Marks |
| **TC3   | source encoding is set to UTF-8 | 4 Marks |

**Total Score: 10 Marks**
