# Snowflake Lab : Snowflake Clustering Keys Optimization

Duration : 60 Min.

## Scenario

Configure custom clustering keys to speed up high-volume filters on Snowflake tables.

## Input Details

The environment has been pre-configured with the following resources:

- **Snowflake Account:** Pre-configured through Service credentials

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Optimized Table:** `opt_table_<normalized_prefix_with_underscores>` (e.g. `OPT_TABLE_STUDENT_EXAM123`)

## Task Objectives

### 1. Configure Clustering Keys

- Alter target table to specify clustering keys.
- Validate micro-partition depth indicators.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                     | Marks   |
| ------------- | ------------------------------- | ------- |
| **TC1** | Clustering key verification     | 5 Marks |
| **TC2** | Micro-partition depth check     | 5 Marks |
| **TC3** | Performance query execution     | 5 Marks |
| **TC4** | Database catalog metadata check | 5 Marks |
| **TC5** | Query plan metrics check        | 5 Marks |

**Total Score: 25 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
