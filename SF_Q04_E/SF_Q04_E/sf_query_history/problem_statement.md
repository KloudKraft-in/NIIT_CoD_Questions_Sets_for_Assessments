# Snowflake Lab : Query History Filtering

Duration : 60 Min.

## Scenario

Inspect historical database queries to check query latency and runtime metrics.

## Input Details

The environment has been pre-configured with the following resources:

- **Snowflake Account:** Pre-configured through Service credentials

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Query History View:** `<prefix>_query_history` (e.g. `student_exam123_query_history`)

## Task Objectives

### 1. Filter Query History

- Execute diagnostic select scripts on internal metadata catalog.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                    | Marks   |
| ------------- | ------------------------------ | ------- |
| **TC1** | SQL query validation           | 4 Marks |
| **TC2** | Filter execution metrics check | 4 Marks |
| **TC3** | Data result verification       | 4 Marks |
| **TC4** | Reserved validation            | 4 Marks |
| **TC5** | Reserved validation            | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
