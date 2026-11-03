# Database Lab : NoSQL Workload Classification & Storage Catalog Setup

Duration : 30 Min.

## Scenario

As a Cloud Data Architect at NIIT, an enterprise microservice platform requires storage category mapping for 4 new workloads. You must establish a workload architecture catalog table in PostgreSQL and populate the recommended storage categories (Key-Value, Document, Wide-Column, Graph).

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **Architecture Catalog Table:** `<prefix>_nosql_catalog`

## Task Objectives

Perform the following configuration steps directly in PostgreSQL via `psql`:

### 1. Create Architecture Catalog Table
- Connect to `localhost:5432` with `psql`.
- Create table `<prefix>_nosql_catalog` with columns:
  - `workload_name VARCHAR(100) PRIMARY KEY`
  - `recommended_category VARCHAR(50) NOT NULL`
  - `representative_engine VARCHAR(50) NOT NULL`
  - `latency_sla VARCHAR(30) NOT NULL`

### 2. Populate Workload Architecture Classifications
- Insert the four enterprise workload mappings:
  1. `('User Session Token Cache', 'Key-Value', 'Redis', '< 1ms')`
  2. `('Product Catalog Dynamic Attributes', 'Document', 'MongoDB', '< 10ms')`
  3. `('Fleet IoT Sensor Time-Series', 'Wide-Column', 'Cassandra', '< 50ms')`
  4. `('Fraud Detection Multi-Hop Traversal', 'Graph', 'Neo4j', '< 25ms')`

### 3. Verify Catalog Consistency
- Run `SELECT * FROM <prefix>_nosql_catalog ORDER BY workload_name;` to confirm records are present.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The verification system inspects the live PostgreSQL database table on `localhost:5432`.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | PostgreSQL Table (<prefix>_nosql_catalog) Creation | 4 Marks |
| **TC2** | NoSQL Category Mapping Population (4 Workloads) | 3 Marks |
| **TC3** | Representative Engine & Latency SLA Accuracy | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- Ensure all 4 workload records are inserted.
