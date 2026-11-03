# Databricks Lab : Spark Broadcast Join Optimization

Duration : 60 Min.

## Scenario

Optimize big data joins by broadcasting a small metadata table to worker nodes, preventing shuffle overhead.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Optimized Table:** `<prefix>_broadcast_join` (e.g. `student_exam123_broadcast_join`)

## Task Objectives

### 1. Implement Broadcast Join
- Write a query broadcasting the smaller table.
- Confirm the broadcast hint in the query physical execution plan.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Join outcome correctness | 4 Marks |
| **TC2** | Broadcast hint check in AST | 4 Marks |
| **TC3** | Optimization execution check | 4 Marks |
| **TC4** | Query plan metrics validation | 4 Marks |
| **TC5** | Output schema structure check | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
