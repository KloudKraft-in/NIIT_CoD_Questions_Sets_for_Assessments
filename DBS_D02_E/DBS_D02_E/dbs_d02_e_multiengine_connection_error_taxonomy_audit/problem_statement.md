# Database Lab : Multi-Engine Connection Error Taxonomy Table Setup

Duration : 30 Min.

## Scenario

As an Infrastructure Support Engineer at NIIT, you receive incoming alerts across four relational engines: Oracle, SQL Server, MySQL, and PostgreSQL. You must establish a centralized error taxonomy table in MySQL, categorizing common error signatures (Authentication, Network, Resource, Configuration).

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **MySQL Service:** `localhost:3306` | DB: `mysql` | User: `root` | Password: `MySQLPassword123!` | CLI: `mysql`
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

When executing database operations:
- **MySQL Taxonomy Table:** `<prefix>_error_taxonomy` (in database `mysql`)

## Task Objectives

Perform the following configuration steps directly via the `mysql` CLI:

### 1. Connect to MySQL Engine
- Connect to `localhost:3306` using the `mysql` CLI with user `root`.

### 2. Create Error Taxonomy Table
- Create a table named `<prefix>_error_taxonomy` in database `mysql` with columns:
  - `error_code VARCHAR(30) PRIMARY KEY`
  - `engine VARCHAR(30) NOT NULL`
  - `category VARCHAR(30) NOT NULL`
  - `remediation_sop TEXT NOT NULL`

### 3. Insert Classified Error Signatures
- Insert the following 4 categorized error signatures:
  1. `('ORA-12541', 'Oracle', 'Network', 'Check TNS listener service status on port 1521')`
  2. `('MSSQL-18456', 'SQL Server', 'Authentication', 'Verify SQL login credentials and account lockout status')`
  3. `('MYSQL-2003', 'MySQL', 'Network', 'Verify mysqld service is running and accepting TCP connections on port 3306')`
  4. `('PG-AUTH-FAIL', 'PostgreSQL', 'Authentication', 'Verify pg_hba.conf rules and password hash for connecting user')`

## Verification

Once you have performed the tasks, run the verification script:
```bash
python run.py
```
The verification system inspects the live MySQL database on `localhost:3306`.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | MySQL Connection & Table (<prefix>_error_taxonomy) Creation | 4 Marks |
| **TC2** | Multi-Engine Error Signature Population (4 Engines) | 3 Marks |
| **TC3** | Category Accuracy (Authentication vs Network) & SOP Details | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix in lowercase.
- Execute SQL commands directly in the mysql console.
