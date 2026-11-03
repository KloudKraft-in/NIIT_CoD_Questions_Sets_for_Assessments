# Snowflake Lab : Snowflake Schema Ingestion

Duration : 60 Min.

## Scenario

Initialize storage structures and databases for raw schema landing.

## Input Details

The environment has been pre-configured with the following resources:

- **Snowflake Account:** Pre-configured through Service credentials

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Database Name:** `admin_db_<normalized_prefix_with_underscores>` (e.g. `ADMIN_DB_STUDENT_EXAM123`)
- **Schema Name:** `raw`

## Task Objectives

### 1. Setup Database & Schema

- Create the database and raw schema.
- Define structural tables.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                        | Marks   |
| ------------- | ---------------------------------- | ------- |
| **TC1** | Database existence check           | 4 Marks |
| **TC2** | Schema existence check             | 4 Marks |
| **TC3** | Table columns structure validation | 4 Marks |
| **TC4** | Reserved validation                | 4 Marks |
| **TC5** | Reserved validation                | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
