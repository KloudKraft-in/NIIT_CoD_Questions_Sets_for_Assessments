# Databricks Lab : Delta Lake Schema Evolution

Duration : 60 Min.

## Scenario

You need to append data with a new schema columns structure to an existing Delta table using schema evolution options.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Delta Table:** `<prefix>_schema_evolution` (e.g. `student_exam123_schema_evolution`)

## Task Objectives

### 1. Ingest and Evolve Schema
- Perform append writes enabling the `mergeSchema` configuration.
- Verify the updated columns set.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Column addition verification | 4 Marks |
| **TC2** | mergeSchema option check | 4 Marks |
| **TC3** | Record validation | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
