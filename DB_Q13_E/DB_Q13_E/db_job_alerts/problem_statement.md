# Databricks Lab : Job Alert Configuration

Duration : 60 Min.

## Scenario

Configure workflow notifications to alert on task failures for production pipelines.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Job Name:** `<prefix>-job-alerts` (e.g. `student-exam123-job-alerts`)

## Task Objectives

### 1. Setup Job Alerts
- Create a workflow job named `<prefix>-job-alerts`.
- Configure email notification triggers on failure events.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Job existence check | 4 Marks |
| **TC2** | Email notification config check | 4 Marks |
| **TC3** | Task binding check | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
