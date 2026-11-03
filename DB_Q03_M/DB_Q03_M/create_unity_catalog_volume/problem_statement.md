# Databricks Lab : Unity Catalog Volume & Data Upload Setup

Duration : 60 Min.

## Scenario

As a Data Engineer at Niit, you are tasked with setting up a secure storage container in the Unity Catalog to store raw business datasets. Your goal is to create a Unity Catalog, establish a schema named `data`, configure a volume named `v1`, and upload a sample CSV data file to be accessed by analytics jobs.

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

### 1. Create Unity Catalog, Schema, and Volume

- **Create Unity Catalog:** Create a catalog named `ut_ltm_<normalized_prefix_with_underscores>`.
- **Create Schema:** Inside the newly created catalog, create a schema named `data`.
- **Create Volume:** Inside the schema `data`, create a volume named `v1`. This volume can be either Managed or External.
- **Upload Dataset:** Upload at least one `.csv` data file into the volume `v1` so that it is accessible at `/Volumes/ut_ltm_<normalized_prefix_with_underscores>/data/v1/`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Databricks Workspace.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Catalog existence (`ut_ltm_<normalized_prefix_with_underscores>` exists) | 4 Marks |
| **TC2** | Schema existence (`data` exists inside the catalog) | 4 Marks |
| **TC3** | Volume existence (`v1` exists inside the schema) | 4 Marks |
| **TC4** | Volume type verification (volume is MANAGED or EXTERNAL) | 4 Marks |
| **TC5** | CSV File presence (at least one `.csv` file exists in the volume directory) | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix.
- The volume path must match the catalog-schema-volume hierarchy.
