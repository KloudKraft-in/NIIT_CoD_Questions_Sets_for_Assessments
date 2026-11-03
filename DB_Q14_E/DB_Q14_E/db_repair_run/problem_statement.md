# Databricks Lab : Failed Job Diagnostic & Repair

Duration : 60 Min.

## Scenario

Diagnose failed runs and trigger the repair utility to retry only the failed tasks in a multi-task pipeline.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Job Name:** `<prefix>-repair-run` (e.g. `student-exam123-repair-run`)

## Task Objectives

### 1. Job Ingress Diagnosis
- Find the failed run id.
- Trigger repair and run retry validation.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | RCA log generated | 4 Marks |
| **TC2** | Repair trigger verification | 4 Marks |
| **TC3** | Task retry logic check | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
