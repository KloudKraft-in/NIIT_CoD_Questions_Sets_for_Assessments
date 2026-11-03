# Airflow Lab : TaskFlow Python Decorator DAG

Duration : 60 Min.

## Scenario

As a Data Platform Engineer at Niit, you are tasked with creating a Directed Acyclic Graph (DAG) using Apache Airflow to automate backend logging jobs. Your objective is to deploy an Airflow DAG leveraging the modern TaskFlow API decorators (`@dag` and `@task`) to print welcome logs and session information.

## Input Details

The environment has been pre-configured with the following resources:
- **Python Environment**: Injected with standard apache-airflow library dependencies.

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` and your exam code is `exam123`, your prefix is **`student-exam123`**.

- **DAG Python File Name:** Create a Python file inside the `student_workspace/` directory (e.g. `decorator_dag.py`).
- **DAG ID:** `decorator_dag_<prefix>` (e.g. `decorator_dag_student_exam123`)

## Task Objectives

Create a Python script in the `student_workspace/` directory implementing the following TaskFlow API requirements:

### 1. Configure the DAG and Tasks
- **DAG Definition:** Use the `@dag` decorator to define your DAG. Assign it the ID `decorator_dag_<prefix>`. Set `schedule_interval=None` and an appropriate start date.
- **Taskflow Decorators:** Use the `@task` decorator to define the tasks.
- **Task 1 (`function1`):** Prints the string `"Welcome orchestrator"`.
- **Task 2 (`function2`):** Prints the string `"Login time"` along with a dynamic timestamp or log output.
- **Dependencies:** Call the tasks sequentially inside the DAG entrypoint function (e.g., `function2(function1())` or similar workflow dependencies).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual Python DAG configuration in the workspace.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Airflow DAG Python Syntax Check (valid compiling script) | 4 Marks |
| **TC2** | DAG Import and DagBag Loading (no import errors) | 4 Marks |
| **TC3** | TaskFlow Decorator API Verification (uses `@dag` and `@task` decorators) | 4 Marks |
| **TC4** | Task 1 Content Verification (`function1` prints "Welcome orchestrator") | 4 Marks |
| **TC5** | Task 2 Content Verification (`function2` prints "Login time") | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Do not modify any files outside the `student_workspace/` directory.
- Ensure the print message strings contain the exact required keywords (case-insensitive).
