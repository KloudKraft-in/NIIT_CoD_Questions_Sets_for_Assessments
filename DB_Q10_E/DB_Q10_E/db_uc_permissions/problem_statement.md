# Databricks Lab : Unity Catalog Schema Permissions

Duration : 60 Min.

## Scenario

You are tasked with setting up schema accessibility and assigning standard permissions within Unity Catalog for raw data ingress.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Schema Name:** `<prefix>_raw_data` (e.g. `student_exam123_raw_data`)

## Task Objectives

### 1. Schema Creation
- Create a schema named `<prefix>_raw_data`.
- Assign appropriate USAGE or SELECT privileges.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Schema existence (`<prefix>_raw_data` exists) | 4 Marks |
| **TC2** | Privilege grant check | 4 Marks |
| **TC3** | Catalog binding check | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
