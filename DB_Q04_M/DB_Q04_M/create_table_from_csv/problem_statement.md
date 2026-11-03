# Databricks Lab : Create Table from CSV File

Duration : 60 Min.

## Scenario

As a Data Engineer at Niit, you need to import external dataset records into your Unity Catalog database for structured analytical queries. Your goal is to ensure the appropriate Unity Catalog and `data` schema exist, and ingest a sample CSV source file into a Delta table within that schema.

## Input Details

The environment has been pre-configured with the following resources:

- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)
- **Resource Group:** `rg-iRUN-LTM-Assessment`

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Catalog Name:** `ut_ltm_<normalized_prefix_with_underscores>` (where the prefix is normalized to lowercase, and any hyphens/dots are replaced with underscores, e.g. `ut_ltm_student_exam123`)

## Task Objectives

Perform the following configuration steps directly in the Databricks Workspace Console or using the Databricks API:

### 1. Ingest Data Table

- **Ensure Catalog and Schema:** Confirm or create the catalog named `ut_ltm_<normalized_prefix_with_underscores>` and the schema named `data` inside it.
- **Ingest Table:** Create a Delta Table inside the schema `ut_ltm_<normalized_prefix_with_underscores>.data` by loading data from any CSV source. The table must contain valid, queryable columns and rows.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Databricks Workspace.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Catalog existence (`ut_ltm_<normalized_prefix_with_underscores>` exists) | 6 Marks |
| **TC2** | Schema existence (`data` exists inside the catalog) | 6 Marks |
| **TC3** | Table Ingestion Check (at least one table exists in `ut_ltm_<normalized_prefix_with_underscores>.data`) | 6 Marks |
| **TC4** | Table Structure Verification (metadata is retrievable, columns defined) | 6 Marks |
| **TC5** | Table Format Validation (format is DELTA or similar structured format) | 6 Marks |

**Total Score: 30 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix.
- The table must contain valid schema metadata and records.
