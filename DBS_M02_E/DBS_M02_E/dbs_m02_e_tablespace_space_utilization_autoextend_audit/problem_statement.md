# Database Lab : Tablespace Capacity Utilization & Autoextend Audit

Duration : 30 Min.

## Scenario

As a Database Capacity Specialist at NIIT, unexpected halts occur when tablespace datafiles reach capacity without autoextend. You must establish a capacity audit table in PostgreSQL, calculate utilized percentages, and flag datafiles requiring expansion.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **Capacity Audit Table:** `<prefix>_tablespace_capacity`

## Task Objectives

Perform the following configuration steps directly via `psql`:

### 1. Create Tablespace Capacity Audit Table
- Create table `<prefix>_tablespace_capacity` with columns:
  - `tablespace_name VARCHAR(50) PRIMARY KEY`
  - `allocated_mb INT NOT NULL`
  - `used_mb INT NOT NULL`
  - `used_pct NUMERIC(5,2) NOT NULL`
  - `autoextend_enabled BOOLEAN NOT NULL`
  - `risk_level VARCHAR(20) NOT NULL`

### 2. Insert Tablespace Risk Metrics
- Insert the following 3 capacity assessments:
  1. `('USERS_TBS', 5000, 2100, 42.00, TRUE, 'LOW')`
  2. `('DATA_TBS', 10000, 9850, 98.50, FALSE, 'CRITICAL')`
  3. `('INDX_TBS', 8000, 4200, 52.50, TRUE, 'MEDIUM')`

### 3. Verify Risk Ranking Query
- Query the critical tablespaces: `SELECT * FROM <prefix>_tablespace_capacity WHERE risk_level = 'CRITICAL';`.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The driver connects to PostgreSQL and validates the capacity audit table.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Capacity Table (<prefix>_tablespace_capacity) Creation | 3 Marks |
| **TC2** | Utilization Metric & Percentage Calculation Population | 3 Marks |
| **TC3** | Autoextend Off Critical Risk Level Flagging | 2 Marks |
| **TC4** | Capacity Risk Ranking & Query Integrity | 2 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- Ensure used_pct matches the allocated and used values.
