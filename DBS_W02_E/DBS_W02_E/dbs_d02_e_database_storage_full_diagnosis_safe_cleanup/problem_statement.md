# Database Lab : PostgreSQL Tablespace Utilization & Safe Vacuum Optimization

Duration : 30 Min.

## Scenario

As a Database Administrator at NIIT, tablespace utilization is growing due to dead tuple bloat. You must create an operational table, seed records, execute a safe `VACUUM ANALYZE` maintenance command, and establish a tablespace audit record.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **Bloat Table:** `<prefix>_bloat_test`
- **Maintenance Audit Table:** `<prefix>_tablespace_audit`

## Task Objectives

Perform the following maintenance steps directly in PostgreSQL via `psql`:

### 1. Create Maintenance Test Table
- Create table `<prefix>_bloat_test (id SERIAL PRIMARY KEY, payload TEXT)`.
- Insert 1,000 sample rows, then update all rows to generate dead tuples.

### 2. Execute Safe Vacuum Maintenance
- Run `VACUUM ANALYZE <prefix>_bloat_test;` to reclaim dead tuple space and refresh planner statistics.

### 3. Record Maintenance Audit
- Create table `<prefix>_tablespace_audit (table_name VARCHAR(100), operation VARCHAR(50), executed_by VARCHAR(50), completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)`.
- Insert a record: `INSERT INTO <prefix>_tablespace_audit VALUES ('<prefix>_bloat_test', 'VACUUM ANALYZE', '<prefix>', CURRENT_TIMESTAMP);`.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The driver queries `pg_stat_user_tables` to assert `last_vacuum` and `last_analyze` timestamps on `<prefix>_bloat_test`.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | PostgreSQL Table (<prefix>_bloat_test) Creation & Dead Tuple Seeding | 4 Marks |
| **TC2** | VACUUM ANALYZE Execution & Catalog Statistics Refresh | 3 Marks |
| **TC3** | Tablespace Maintenance Audit (<prefix>_tablespace_audit) Recording | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- VACUUM command must complete successfully on the live database.
