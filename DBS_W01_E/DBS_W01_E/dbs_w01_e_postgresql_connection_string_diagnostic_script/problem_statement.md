# Database Lab : PostgreSQL Connection String Diagnostic Automation

Duration : 30 Min.

## Scenario

As a Database Engineer at NIIT, microservice deployment scripts frequently fail due to malformed PostgreSQL connection strings. You must author a diagnostic Python script `test_pg_dsn.py` that validates TCP port 5432 reachability and executes a database version query.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Deliverable in `student_workspace/`:
- **Diagnostic Script:** `test_pg_dsn.py`

## Task Objectives

Author a Python diagnostic script `test_pg_dsn.py` inside `student_workspace/` that performs:

### 1. Socket Pre-Flight Check
- Implement a TCP socket reachability test confirming port 5432 on `localhost` is listening.

### 2. Live Database Handshake
- Connect to PostgreSQL (`localhost:5432`, db: `postgres`, user: `postgres`, password: `PostgresPassword123!`) using `psycopg2`.

### 3. Query Execution & Diagnostic Output
- Execute `SELECT current_database(), current_user, version();` and print the output string.

## Verification

Run the verification script:
```bash
python run.py
```
The driver executes your script and validates socket testing and query output.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | test_pg_dsn.py Creation & TCP Socket Verification | 4 Marks |
| **TC2** | PostgreSQL Live Driver Handshake on Port 5432 | 3 Marks |
| **TC3** | Query Execution (current_database & version) Output | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Ensure test_pg_dsn.py executes cleanly without errors.
- Use standard Python libraries (socket, psycopg2).
