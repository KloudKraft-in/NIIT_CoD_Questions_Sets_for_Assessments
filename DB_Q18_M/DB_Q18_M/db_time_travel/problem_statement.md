# Databricks Lab : Delta Lake Time Travel & Restore

Duration : 60 Min.

## Scenario

Utilize Delta transaction log details to perform time travel queries and restore a table to a prior state.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Delta Table:** `<prefix>_time_travel` (e.g. `student_exam123_time_travel`)

## Task Objectives

### 1. Delta Time Travel
- Execute RESTORE query targeting version timestamps or indexes.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Version check validation | 4 Marks |
| **TC2** | Restore query execution | 4 Marks |
| **TC3** | Row count matching | 4 Marks |
| **TC4** | Data consistency check | 4 Marks |
| **TC5** | History logs presence | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
