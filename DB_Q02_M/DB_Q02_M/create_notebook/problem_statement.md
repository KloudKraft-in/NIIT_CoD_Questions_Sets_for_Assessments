# Databricks Lab : Workspace Directory & Notebook Setup

Duration : 60 Min.

## Scenario

As a Junior Data Engineer at Niit, you are tasked with provisioning a shared development space and template notebook for your data science team. Your objective is to create a workspace directory and initialize a Python template notebook with an interactive greeting script.

## Input Details

The environment has been pre-configured with the following resources:

- **Workspace:** Pre-configured through Niit Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)
- **Resource Group:** `rg-iRUN-LTM-Assessment`

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Workspace Directory Path:** `/Shared/<prefix>-workspace` (e.g. `/Shared/student-exam123-workspace`)
- **Notebook Name:** `data-analysis`

## Task Objectives

Perform the following configuration steps directly in the Databricks Workspace Console or using the Databricks API:

### 1. Create Workspace Directory & Notebook

- **Create Workspace Directory:** Create a directory named `/Shared/<prefix>-workspace` under the `Shared` folder (e.g. `/Shared/student-exam123-workspace`).
- **Create Template Notebook:** Inside the directory `/Shared/<prefix>-workspace`, create a notebook named `data-analysis`.
- **Configure Notebook Language:** Set the default language of the notebook to **Python**.
- **Initialize Interactive Code:** Write a Python script in the notebook that:
  - Prompts the user to enter their name using the `input()` function.
  - Prints the welcome message: `Welcome to Niit Databricks Workspace, <name>!` (where `<name>` is the dynamic value supplied via input).

Example snippet for the notebook content:
```python
name = input("Enter your name: ")
print(f"Welcome to Niit Databricks Workspace, {name}!")
```

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Databricks Workspace.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Directory existence (`/Shared/<prefix>-workspace` exists) | 4 Marks |
| **TC2** | Notebook existence (`/Shared/<prefix>-workspace/data-analysis` exists) | 4 Marks |
| **TC3** | Object Type verification (path resolves to a notebook object) | 4 Marks |
| **TC4** | Notebook Language (language is PYTHON) | 4 Marks |
| **TC5** | Interactive Code Check (uses `input()` and prints "Welcome to Niit Databricks Workspace") | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- The notebook path must exactly match the naming convention.
