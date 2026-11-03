# Databricks Lab : Spark Z-Ordering & Partitioning

Duration : 60 Min.

## Scenario

Perform data file compaction and layout co-locality optimization using Partitioning and Z-Ordering.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Optimized Table:** `<prefix>_zorder_optimize` (e.g. `student_exam123_zorder_optimize`)

## Task Objectives

### 1. Partition and Z-Order
- Compact files and structure partitions.
- Execute Z-ORDER BY query on key columns.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Partition layout check | 4 Marks |
| **TC2** | Z-order layout metadata check | 4 Marks |
| **TC3** | Query run metrics check | 4 Marks |
| **TC4** | Compaction optimization index | 4 Marks |
| **TC5** | Pruning evaluation check | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
