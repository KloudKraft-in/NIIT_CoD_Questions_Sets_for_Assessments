# Database Lab : Multi-Engine CLI Connectivity & Health Sign-Off

Duration : 30 Min.

## Scenario

As a Database Engineer at NIIT, before a new environment goes live, you must confirm connectivity to the database engines in the estate using their native CLI tools (`psql` and `mysql`), create environment sign-off markers, and verify read/write access.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`
- **MySQL:** `localhost:3306` | DB: `mysql` | User: `root` | Password: `MySQLPassword123!` | CLI: `mysql`
- **SQL Server:** `localhost:1433` | CLI: `sqlcmd`
- **Oracle XE:** `localhost:1521` | CLI: `sqlplus`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **PostgreSQL Table:** `<prefix>_cli_audit` (in database `postgres`)
- **MySQL Database:** `<prefix>_cli_audit_db`

## Task Objectives

Perform the following configuration steps directly via native database CLIs:

### 1. PostgreSQL CLI Sign-Off (`psql`)
- Connect to PostgreSQL using `psql`.
- Create a sign-off table named `<prefix>_cli_audit` with columns `(id SERIAL PRIMARY KEY, engine VARCHAR(30), verified_by VARCHAR(50), checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)`.
- Insert a sign-off row: `INSERT INTO <prefix>_cli_audit (engine, verified_by) VALUES ('PostgreSQL', '<prefix>');`.

### 2. MySQL CLI Sign-Off (`mysql`)
- Connect to MySQL using `mysql` CLI.
- Create a sign-off database named `<prefix>_cli_audit_db`.
- Inside `<prefix>_cli_audit_db`, create a table named `readiness_check (engine VARCHAR(30), status VARCHAR(20))`.
- Insert a row: `INSERT INTO readiness_check VALUES ('MySQL', 'READY');`.

### 3. Verify Database Read Access
- Run SELECT queries in both `psql` and `mysql` to confirm records are queryable.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The verification system inspects both PostgreSQL (`localhost:5432`) and MySQL (`localhost:3306`) live databases.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | PostgreSQL psql Connection & <prefix>_cli_audit Table Creation | 4 Marks |
| **TC2** | MySQL CLI Connection & <prefix>_cli_audit_db Database Creation | 3 Marks |
| **TC3** | Sign-Off Record Insertion & Verification across Engines | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- Ensure database names and table names match the exact naming conventions.
