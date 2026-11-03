# Database Lab : Tablespace Full Emergency Triage & Space Reclamation

Duration : 60 Min.

## Scenario

As a Principal Database Operations Engineer at NIIT, production transactions are failing due to tablespace exhaustion. You must execute emergency triage in PostgreSQL, perform vacuum operations to reclaim space, and create an emergency space reclamation audit table.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **Emergency Audit Table:** `<prefix>_emergency_space_audit`

## Task Objectives

Perform the following configuration and space reclamation steps via `psql`:

### 1. Interrogate Database & Tablespace Sizes
- Connect via `psql` and execute:
  ```sql
  SELECT pg_size_pretty(pg_database_size('postgres'));
  ```

### 2. Create Emergency Audit Table
- Create table `<prefix>_emergency_space_audit` with columns:
  - `audit_id SERIAL PRIMARY KEY`
  - `failing_tablespace VARCHAR(50) NOT NULL`
  - `reclaimed_mb INT NOT NULL`
  - `purge_action TEXT NOT NULL`
  - `alert_threshold_pct INT NOT NULL`
  - `audited_by VARCHAR(50) NOT NULL`

### 3. Record Space Reclamation Actions
- Insert an audit entry logging `failing_tablespace = 'pg_default'`, `reclaimed_mb = 12000`, `purge_action = 'VACUUM FULL & TEMP PURGE'`, `alert_threshold_pct = 85`, and `audited_by = '<prefix>'`.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The driver connects to PostgreSQL, evaluates database size queries, and inspects the emergency audit table.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Database Size Query Execution (pg_database_size) | 3 Marks |
| **TC2** | Emergency Audit Table (<prefix>_emergency_space_audit) Creation | 3 Marks |
| **TC3** | Reclaimed Space Metric Documentation | 3 Marks |
| **TC4** | Purge Action SOP & Datafile Maintenance Verification | 3 Marks |
| **TC5** | Capacity Threshold Alert Configuration (85% Limit) | 2 Marks |
| **TC6** | Tablespace Metadata & Location Inspection | 2 Marks |
| **TC7** | Audited By Prefix Integrity Check | 2 Marks |
| **TC8** | Live Database Storage-Full Recovery Sign-Off | 2 Marks |

**Total Score: 20 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- All actions must be executed in the live PostgreSQL instance.
