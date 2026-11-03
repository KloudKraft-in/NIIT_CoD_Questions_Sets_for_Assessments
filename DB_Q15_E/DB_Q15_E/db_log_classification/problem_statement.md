# Databricks Lab : Cluster Diagnostic Log Parsing

Duration : 60 Min.

## Scenario

Create a parser to process cluster diagnostics event logs, classifying logs into severity buckets.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Log Utility Name:** `<prefix>_log_classification` (e.g. `student_exam123_log_classification`)

## Task Objectives

### 1. Build Parser Utility
- Parse cluster driver logs.
- Categorize and output errors.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Log utility script validation | 4 Marks |
| **TC2** | Error event parsing | 4 Marks |
| **TC3** | Class outcome verification | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
