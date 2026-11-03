# Databricks Lab : Real-Time vs Batch Routing

Duration : 60 Min.

## Scenario

You are tasked with setting up a real-time data routing view to filter high-value sales events from the primary sales dataset.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Routing View:** `<prefix>_realtime_high_value_sales` (e.g. `student_exam123_realtime_high_value_sales`)

## Task Objectives

### 1. Create Routing View
- Create a view named `<prefix>_realtime_high_value_sales` filtering records with high value.
- Ensure it references the core sales data source correctly.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | View existence (`<prefix>_realtime_high_value_sales` exists) | 4 Marks |
| **TC2** | Filtering logic check (high value threshold filter) | 4 Marks |
| **TC3** | View base table dependency | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
