# Databricks Lab : Multitask Job Pipeline Setup

Duration : 60 Min.

## Scenario

Build a multi-task workflow pipeline defining dependencies, failure retries, and task parameters.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Multitask Job:** `<prefix>-multitask-job` (e.g. `student-exam123-multitask-job`)

## Task Objectives

### 1. Create Workflow Job
- Set task sequence dependencies.
- Add task parameters.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Job layout check | 4 Marks |
| **TC2** | Upstream task dependencies definition | 4 Marks |
| **TC3** | Parameter parsing validation | 4 Marks |
| **TC4** | Task running sequences | 4 Marks |
| **TC5** | Failure notification check | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
