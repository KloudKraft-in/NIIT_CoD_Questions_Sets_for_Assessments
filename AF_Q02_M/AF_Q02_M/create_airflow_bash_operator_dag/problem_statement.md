# Airflow Lab : BashOperator DAG with Date & Time

Duration : 60 Min.

## Scenario

As a Data Platform Engineer at Niit, you are tasked with creating a Directed Acyclic Graph (DAG) using Apache Airflow to run automated operating system metrics collections. Your objective is to deploy an Airflow DAG leveraging the standard `BashOperator` to print a welcome message and log the current system date and time.

## Input Details

The environment has been pre-configured with the following resources:
- **Python Environment**: Injected with standard apache-airflow library dependencies.

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` and your exam code is `exam123`, your prefix is **`student-exam123`**.

- **DAG Python File Name:** Create a Python file inside the `student_workspace/` directory (e.g. `bash_dag.py`).
- **DAG ID:** `bash_dag_<prefix>` (e.g. `bash_dag_student_exam123`)

## Task Objectives

Create a Python script in the `student_workspace/` directory implementing the following BashOperator requirements:

### 1. Configure the DAG and Tasks
- **DAG Definition:** Assign the DAG the ID `bash_dag_<prefix>`. Set `schedule_interval=None` and an appropriate start date.
- **Operator Selection:** Use the `BashOperator` to define exactly two tasks.
- **Task 1:** Runs the bash command `echo "Welcome to Airflow"`.
- **Task 2:** Runs the bash command `date` (which displays the current system date and time).
- **Dependencies:** Define a sequential execution dependency between the two tasks (e.g. `task1 >> task2`).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual Python DAG configuration in the workspace.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Airflow DAG Python Syntax Check (valid compiling script) | 4 Marks |
| **TC2** | DAG Import and DagBag Loading (no import errors) | 4 Marks |
| **TC3** | BashOperator Tasks Class Check (at least 2 tasks are BashOperators) | 4 Marks |
| **TC4** | Task 1 Command Verification (runs `echo "Welcome to Airflow"`) | 4 Marks |
| **TC5** | Task 2 Command Verification (runs `date`) | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Do not modify any files outside the `student_workspace/` directory.
- Ensure the bash commands match the requirements exactly.
