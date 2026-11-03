# Snowflake Lab : Database and Schema Setup

Duration : 60 Min.

## Scenario

As a Junior Data Engineer at Niit, you are tasked with setting up a clean database environment in Snowflake for importing commercial datasets. Your objective is to create a Snowflake database, establish a schema named `DATA` inside it, load records from a CSV source, and run verification query statements.

## Input Details

The environment has been pre-configured with the following resources:
- **Snowflake Account:** Pre-configured through Niit Service credentials (`SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_WAREHOUSE`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Database Name:** `sn_ltm_<normalized_prefix_with_underscores>` (where the prefix is normalized to lowercase, any dots replaced with hyphens, and then all hyphens replaced with underscores, and converted to uppercase in Snowflake, e.g. `SN_LTM_STUDENT_EXAM123`)

## Task Objectives

Perform the following configuration steps directly in the Snowflake Worksheet or Web Console:

### 1. Configure Snowflake Database & Schema

- **Create Database:** Create a database named `SN_LTM_<normalized_prefix_with_underscores>`.
- **Create Schema:** Create a schema named `DATA` inside the newly created database.
- **Table and Data Load:** Create a table within the `DATA` schema and load a sample CSV dataset's records into it.
- **Query Dataset:** Execute analytical queries (e.g. `SELECT` statements) to retrieve and verify table records.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Snowflake cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Database existence (`SN_LTM_<normalized_prefix_with_underscores>` exists) | 4 Marks |
| **TC2** | Schema existence (`DATA` exists inside the database) | 4 Marks |
| **TC3** | Table Ingestion Check (at least one table exists in the schema) | 4 Marks |
| **TC4** | Table Column Verification (columns metadata can be fetched) | 4 Marks |
| **TC5** | Table Data Verification (ingested table has non-empty row count) | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all database and schema names exactly match the naming convention.
- Loaded table must contain queryable fields and data rows.
