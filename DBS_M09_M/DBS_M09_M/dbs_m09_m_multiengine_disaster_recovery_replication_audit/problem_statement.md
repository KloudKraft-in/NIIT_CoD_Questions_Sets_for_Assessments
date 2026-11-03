# Database Lab : Disaster Recovery Replication Governance & Failover Quorum

Duration : 60 Min.

## Scenario

As a Global Disaster Recovery Lead at NIIT, primary region telemetry indicates potential network partitioning across multi-engine database pairs. You must establish a disaster recovery governance table in MySQL, defining RPO/RTO thresholds, automatic failover eligibility, and split-brain fencing policies.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **MySQL Service:** `localhost:3306` | DB: `mysql` | User: `root` | Password: `MySQLPassword123!` | CLI: `mysql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **MySQL DR Table:** `mysql.<prefix>_dr_governance`

## Task Objectives

Perform the following configuration steps directly via `mysql` CLI:

### 1. Create DR Governance Table
- In MySQL, create table `mysql.<prefix>_dr_governance` with columns:
  - `dr_pair_id VARCHAR(50) PRIMARY KEY`
  - `engine VARCHAR(30) NOT NULL`
  - `rpo_sla_seconds INT NOT NULL`
  - `rto_sla_seconds INT NOT NULL`
  - `fencing_mechanism VARCHAR(50) NOT NULL`
  - `auto_failover_eligible BOOLEAN NOT NULL`
  - `certified_by VARCHAR(50) NOT NULL`

### 2. Populate Multi-Engine DR Specifications
- Insert the following 3 disaster recovery pair governance entries:
  1. `('DR-PG-PRIMARY', 'PostgreSQL 16', 10, 60, 'STONITH_WITNESS', TRUE, '<prefix>')`
  2. `('DR-MY-PRIMARY', 'MySQL 8.0', 10, 60, 'RAFT_QUORUM', TRUE, '<prefix>')`
  3. `('DR-MS-PRIMARY', 'SQL Server', 10, 60, 'CLUSTER_MAJORITY', TRUE, '<prefix>')`

### 3. Verify DR Policies Query
- Run `SELECT * FROM mysql.<prefix>_dr_governance WHERE auto_failover_eligible = TRUE;`.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The driver connects to MySQL on `localhost:3306` and validates the DR governance table.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | MySQL DR Governance Table (<prefix>_dr_governance) Creation | 3 Marks |
| **TC2** | Multi-Engine DR Specification Population (Postgres, MySQL, MSSQL) | 3 Marks |
| **TC3** | RPO (<10s) and RTO (<60s) SLA Standards Enforcement | 3 Marks |
| **TC4** | Fencing Mechanism (STONITH / Quorum) Policy Definition | 3 Marks |
| **TC5** | Automatic Failover Eligibility Rules Specification | 2 Marks |
| **TC6** | Split-Brain Prevention Controls Verification | 2 Marks |
| **TC7** | Certified By Prefix Integrity Check | 2 Marks |
| **TC8** | End-to-End DR Replication Governance Sign-Off | 2 Marks |

**Total Score: 20 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- All commands must be run in the live mysql console.
