# Databricks Lab : Delta Lake VACUUM & Retention Policy Management

Duration : 60 Min.

## Scenario

Configure custom table retention values and execute the VACUUM command to purge untracked transactional files.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Delta Table:** `<prefix>_vacuum_retention` (e.g. `student_exam123_vacuum_retention`)

## Task Objectives

### 1. Vacuum & Retention Settings
- Override safety checks and run VACUUM.
- Set retention interval policies.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Table existence verification | 5 Marks |
| **TC2** | Override configuration check (invalidRetentionDurationCheck disable) | 5 Marks |
| **TC3** | VACUUM execution check | 5 Marks |
| **TC4** | Purged data files verification | 5 Marks |
| **TC5** | Table history metadata retention check | 5 Marks |

**Total Score: 25 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
