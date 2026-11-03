# Databricks Lab : Workspace Navigation & Setup

Duration : 60 Min.

## Scenario

As a Junior Data Engineer at Niit, you are tasked with initializing a new workspace folder structure and metadata configuration. This workspace environment will store and track all data pipelines for your team.

## Input Details

The environment has been pre-configured with the following resources:
- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Workspace Directory:** `/Shared/<prefix>-workspace` (e.g. `/Shared/student-exam123-workspace`)
- **Metadata File:** `metadata.json` placed inside the directory.

## Task Objectives

### 1. Create Workspace Folder
- Create a directory in the workspace path `/Shared/<prefix>-workspace`.

### 2. Configure Metadata File
- Create a file named `metadata.json` inside the directory.
- Set its content to valid JSON containing key structural configurations for your pipelines.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Directory existence (`/Shared/<prefix>-workspace` exists) | 4 Marks |
| **TC2** | Metadata file presence (`metadata.json` exists in the folder) | 4 Marks |
| **TC3** | Metadata structure validation (valid JSON content) | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
