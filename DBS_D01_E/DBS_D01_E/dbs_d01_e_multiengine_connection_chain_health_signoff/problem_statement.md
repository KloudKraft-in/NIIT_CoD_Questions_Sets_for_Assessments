# Database Lab : Multi-Engine Connection Chain Health Sign-Off

Duration : 30 Min.

## Scenario

As a Database Support Engineer at NIIT, you are tasked with verifying and signing off the 5-layer connection chain (Client, Connection Pool, Network Connection, Database Session, SQL Statement) across the database engines running on your local Ubuntu Linux environment.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`
- **MySQL Service:** `localhost:3306` | DB: `mysql` | User: `root` | Password: `MySQLPassword123!` | CLI: `mysql`
- **SQL Server Service:** `localhost:1433` | DB: `master` | User: `sa` | Password: `MSSQLPassword123!` | CLI: `sqlcmd`
- **Oracle XE Service:** `localhost:1521/XEPDB1` | User: `system` | Password: `OraclePassword123!` | CLI: `sqlplus`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

When executing database operations:
- **PostgreSQL Audit Table:** `<prefix>_conn_chain`

## Task Objectives

Perform the following configuration steps directly via the platform CLI tools (`psql`, `mysql`, `sqlcmd`, `sqlplus`):

### 1. PostgreSQL Connection Chain Verification (`psql`)
- Connect to PostgreSQL (`localhost:5432`) using `psql` with user `postgres`.
- Create a sign-off audit table named `<prefix>_conn_chain` with columns:
  - `id SERIAL PRIMARY KEY`
  - `layer_name VARCHAR(50) NOT NULL`
  - `status VARCHAR(20) NOT NULL`
  - `signed_by VARCHAR(50) NOT NULL`
  - `verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`

### 2. Populate Interaction Layer Audit Records
- Insert 5 distinct records into `<prefix>_conn_chain` logging all five interaction layers with `status = 'HEALTHY'` and `signed_by = '<prefix>'`:
  1. `Client Runtime`
  2. `Connection Pool`
  3. `Network Connection`
  4. `Database Session`
  5. `SQL Statement Execution`

### 3. Verify Database Engine Read Access
- Execute a query against `<prefix>_conn_chain` to verify that all 5 layers are recorded and queryable.

## Verification

Once you have performed the tasks, run the verification script from your workspace:
```bash
python run.py
```
The verification system checks the actual live database platform on `localhost:5432`.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | PostgreSQL Connection & Table (<prefix>_conn_chain) Creation | 4 Marks |
| **TC2** | 5-Layer Connection Chain Audit Records Population | 3 Marks |
| **TC3** | Data Integrity & Candidate Sign-Off Verification | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your actual candidate prefix in lowercase.
- All operations must be performed on the live database using psql.
