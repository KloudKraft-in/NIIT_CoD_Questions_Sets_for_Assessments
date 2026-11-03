# Database Lab : Cross-Engine Connection DSN & Parameter Audit Table

Duration : 30 Min.

## Scenario

As a Cloud Platform Engineer at NIIT, corporate security mandates that all database DSNs across Oracle, SQL Server, MySQL, and PostgreSQL enforce encryption and standard ports. You must establish an audit table in PostgreSQL and populate the DSN compliance status.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **DSN Audit Table:** `<prefix>_dsn_audit`

## Task Objectives

Perform the following configuration steps directly via `psql`:

### 1. Create DSN Audit Table
- In PostgreSQL, create table `<prefix>_dsn_audit` with columns:
  - `dsn_id VARCHAR(50) PRIMARY KEY`
  - `engine VARCHAR(30) NOT NULL`
  - `port INT NOT NULL`
  - `tls_enabled BOOLEAN NOT NULL`
  - `compliance_status VARCHAR(20) NOT NULL`

### 2. Populate DSN Compliance Records
- Insert 4 audit entries across the engines:
  1. `('DSN-PG-01', 'PostgreSQL', 5432, TRUE, 'COMPLIANT')`
  2. `('DSN-MY-01', 'MySQL', 3306, TRUE, 'COMPLIANT')`
  3. `('DSN-MS-01', 'SQL Server', 1433, FALSE, 'NON_COMPLIANT')`
  4. `('DSN-OR-01', 'Oracle', 1521, TRUE, 'COMPLIANT')`

### 3. Verify Table Read Access
- Run `SELECT * FROM <prefix>_dsn_audit WHERE compliance_status = 'COMPLIANT';`.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The driver connects to PostgreSQL and validates the `<prefix>_dsn_audit` table.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | PostgreSQL DSN Audit Table (<prefix>_dsn_audit) Creation | 3 Marks |
| **TC2** | Multi-Engine DSN Compliance Records Population (4 Engines) | 3 Marks |
| **TC3** | Standard Port Validation (5432, 3306, 1433, 1521) | 2 Marks |
| **TC4** | TLS / SSL Compliance Status Differentiation | 2 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- Ensure all 4 rows are inserted.
