# Databricks Lab : Delta Table Autoloader Ingestion

Duration : 60 Min.

## Scenario

Deploy an Auto Loader stream configuration to incrementally ingest cloud storage data.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Delta Table:** `<prefix>_autoloader_ingest` (e.g. `student_exam123_autoloader_ingest`)

## Task Objectives

### 1. Auto Loader Configuration
- Set up structured streaming with cloudFiles source.
- Ingest to `<prefix>_autoloader_ingest` Delta table.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Table load check | 4 Marks |
| **TC2** | Auto Loader config check | 4 Marks |
| **TC3** | Schema schemaLocation validation | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
