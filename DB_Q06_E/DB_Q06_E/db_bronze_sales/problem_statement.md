# Databricks Lab : Lakehouse Ingestion Layer

Duration : 60 Min.

## Scenario

As a Junior Data Engineer, you need to create the initial ingestion layer (Bronze) in your Delta Lake. You will set up the target Delta table structure to ingest raw sales records.

## Input Details

The environment has been pre-configured with the following resources:

- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Delta Table:** `<prefix>_bronze_sales` (e.g. `student_exam123_bronze_sales` or under default schema)

## Task Objectives

### 1. Create Bronze Sales Table

- Create a Delta table named `<prefix>_bronze_sales` (use underscores in place of hyphens if required by SQL catalog rules).
- Ensure it defines fields for transaction tracking.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                               | Marks   |
| ------------- | --------------------------------------------------------- | ------- |
| **TC1** | Delta table existence (`<prefix>_bronze_sales` exists)  | 4 Marks |
| **TC2** | Schema columns check (columns match required definitions) | 4 Marks |
| **TC3** | Delta format confirmation                                 | 4 Marks |
| **TC4** | Reserved validation                                       | 4 Marks |
| **TC5** | Reserved validation                                       | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
