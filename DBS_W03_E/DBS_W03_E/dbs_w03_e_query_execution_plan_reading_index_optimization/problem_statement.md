# Database Lab : Live Query Execution Plan Tuning – Seq Scan to Index Scan

Duration : 30 Min.

## Scenario

As a Query Optimization Specialist at NIIT, a high-volume transactions query is performing an unindexed Sequential Table Scan. You must populate sample transaction records in PostgreSQL, analyze the plan via `EXPLAIN`, create a composite B-Tree index, and assert the plan transitions to an `Index Scan`.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **Transactions Table:** `<prefix>_txns`
- **Composite Index:** `idx_<prefix>_txns_acct_date`

## Task Objectives

Perform the following optimization steps directly via `psql`:

### 1. Create & Seed Transactions Table
- Create table `<prefix>_txns` with columns:
  - `id SERIAL PRIMARY KEY`
  - `account_id INT NOT NULL`
  - `txn_date DATE NOT NULL`
  - `amount NUMERIC(10,2) NOT NULL`
- Insert at least 500 records into `<prefix>_txns`.

### 2. Create Composite Index
- Create a composite B-Tree index named `idx_<prefix>_txns_acct_date` on `<prefix>_txns (account_id, txn_date)`.

### 3. Verify Execution Plan
- Run `EXPLAIN SELECT * FROM <prefix>_txns WHERE account_id = 100 AND txn_date = '2026-10-01';` and verify that PostgreSQL uses `Index Scan` or `Bitmap Index Scan` instead of `Seq Scan`.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The driver connects to PostgreSQL, inspects `pg_indexes`, and executes `EXPLAIN` to verify the active plan operator.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Table (<prefix>_txns) Creation & Record Seeding | 4 Marks |
| **TC2** | Composite B-Tree Index (idx_<prefix>_txns_acct_date) Creation | 3 Marks |
| **TC3** | Execution Plan Verification (Index Scan Operator Transition) | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- Ensure the composite index contains both `account_id` and `txn_date`.
