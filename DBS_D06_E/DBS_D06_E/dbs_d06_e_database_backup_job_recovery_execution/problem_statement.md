# Database Lab : Database Backup Execution & Audit Log Setup

Duration : 30 Min.

## Scenario

As a Database Reliability Engineer at NIIT, after a failed backup alert, you must execute a schema backup of PostgreSQL using `pg_dump`, store the backup artifact in the backup directory, and record a backup audit log entry in the database.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`
- **Backup Directory:** `/var/backups/db/` (or `~/backups/`)

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **Backup Target Directory:** `/var/backups/db/<prefix>_backup/` (or `~/backups/<prefix>_backup/`)
- **Backup File:** `postgres_schema.sql`
- **PostgreSQL Audit Table:** `<prefix>_backup_audit`

## Task Objectives

Perform the following backup and audit steps:

### 1. Create Backup Target Directory
- Create directory `/var/backups/db/<prefix>_backup/` (or `~/backups/<prefix>_backup/` if permissions require).

### 2. Execute pg_dump Schema Backup
- Run `pg_dump` to generate a schema-only backup of database `postgres`:
  ```bash
  PGPASSWORD='PostgresPassword123!' pg_dump -h localhost -U postgres -d postgres --schema-only -f /var/backups/db/<prefix>_backup/postgres_schema.sql
  ```

### 3. Record Backup Audit in Database
- Connect via `psql` and create table `<prefix>_backup_audit` with columns:
  - `backup_id SERIAL PRIMARY KEY`
  - `backup_file VARCHAR(200) NOT NULL`
  - `backup_type VARCHAR(30) NOT NULL`
  - `status VARCHAR(20) NOT NULL`
  - `logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- Insert a record logging `backup_file = 'postgres_schema.sql'`, `backup_type = 'SCHEMA_ONLY'`, and `status = 'COMPLETED'`.

## Verification

Once you have performed the tasks, run the verification script:
```bash
python run.py
```
The verification system checks the backup file on disk and inspects the database audit table.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Backup Directory & Target Path Configuration | 4 Marks |
| **TC2** | pg_dump Schema Backup File Generation on Disk | 3 Marks |
| **TC3** | Database Backup Audit Table & Sign-Off Record | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- Ensure the output SQL file contains valid PostgreSQL DDL statements.
