# Databricks Lab : Delta Lake OPTIMIZE Command

Duration : 60 Min.

## Scenario

You need to perform performance optimization on a Delta table containing fragmented files using the OPTIMIZE command.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Delta Table:** `<prefix>_optimize_table` (e.g. `student_exam123_optimize_table`)

## Task Objectives

### 1. Table Optimization
- Create a Delta table named `<prefix>_optimize_table`.
- Execute the `OPTIMIZE` statement to compact small files.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Delta table compact files check | 4 Marks |
| **TC2** | Query history compaction log verify | 4 Marks |
| **TC3** | Schema integrity validation | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
