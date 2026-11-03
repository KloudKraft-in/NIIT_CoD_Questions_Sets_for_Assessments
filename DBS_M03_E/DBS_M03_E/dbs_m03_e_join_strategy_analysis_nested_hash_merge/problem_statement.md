# Database Lab : Relational Join Strategy & Plan Analysis Setup

Duration : 30 Min.

## Scenario

As a Query Optimization Engineer at NIIT, an enterprise reporting query linking departments and employees requires performance tuning. You must create two relational tables with primary/foreign keys in PostgreSQL, populate sample records, and record the optimizer's join strategy in an audit table.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **Departments Table:** `<prefix>_depts`
- **Employees Table:** `<prefix>_emps`
- **Join Audit Table:** `<prefix>_join_strategy_audit`

## Task Objectives

Perform the following configuration steps directly via `psql`:

### 1. Create Relational Tables with Keys
- Create `<prefix>_depts (dept_id INT PRIMARY KEY, dept_name VARCHAR(50) NOT NULL)`.
- Create `<prefix>_emps (emp_id SERIAL PRIMARY KEY, dept_id INT REFERENCES <prefix>_depts(dept_id), emp_name VARCHAR(50) NOT NULL, salary NUMERIC(10,2))`.
- Insert 3 departments and 10 employee rows.

### 2. Create Join Strategy Audit Table
- Create table `<prefix>_join_strategy_audit` with columns:
  - `id SERIAL PRIMARY KEY`
  - `join_type VARCHAR(30) NOT NULL`
  - `operator_name VARCHAR(30) NOT NULL`
  - `tested_by VARCHAR(50) NOT NULL`

### 3. Record Plan Operator Verification
- Insert a record logging `join_type = 'INNER JOIN'`, `operator_name = 'Hash Join'`, and `tested_by = '<prefix>'`.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The driver connects to PostgreSQL, validates the foreign key relationships, and checks the join audit table.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Primary & Foreign Key Tables (<prefix>_depts, <prefix>_emps) Creation | 3 Marks |
| **TC2** | Data Seeding & Referential Integrity Verification | 3 Marks |
| **TC3** | Join Audit Table (<prefix>_join_strategy_audit) Setup | 2 Marks |
| **TC4** | Join Operator (Hash Join vs Nested Loop) Verification | 2 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- Foreign key constraint must be active.
