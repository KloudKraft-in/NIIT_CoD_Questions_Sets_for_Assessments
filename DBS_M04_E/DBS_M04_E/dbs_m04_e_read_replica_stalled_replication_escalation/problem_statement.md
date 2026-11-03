# Database Lab : Read Replica Stalled Replication Escalation Table

Duration : 30 Min.

## Scenario

As a Database Platform Engineer at NIIT, a disaster recovery replica has stalled. You must create an incident escalation table in MySQL and record time-series lag markers and root causes to notify the platform on-call team.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **MySQL Service:** `localhost:3306` | DB: `mysql` | User: `root` | Password: `MySQLPassword123!` | CLI: `mysql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **MySQL Table:** `<prefix>_replica_escalation` (in database `mysql`)

## Task Objectives

Perform the following configuration steps directly via `mysql` CLI:

### 1. Create Replication Escalation Table
- In MySQL, create table `mysql.<prefix>_replica_escalation` with columns:
  - `ticket_id VARCHAR(30) PRIMARY KEY`
  - `replica_id VARCHAR(50) NOT NULL`
  - `lag_seconds INT NOT NULL`
  - `stall_status VARCHAR(30) NOT NULL`
  - `priority VARCHAR(10) NOT NULL`
  - `escalated_by VARCHAR(50) NOT NULL`

### 2. Record Incident Escalation Data
- Insert an escalation entry:
  `INSERT INTO mysql.<prefix>_replica_escalation VALUES ('INC-84910', 'replica-dr-01', 2700, 'STALLED_REPLAY', 'P1', '<prefix>');`

### 3. Verify Escalation Query
- Run `SELECT * FROM mysql.<prefix>_replica_escalation WHERE priority = 'P1';`.

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The driver connects to MySQL on `localhost:3306` and validates the table.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | MySQL Table (<prefix>_replica_escalation) Creation | 3 Marks |
| **TC2** | Replication Stall Metrics (Lag Seconds, Status) Population | 3 Marks |
| **TC3** | Severity Priority (P1) Categorization | 2 Marks |
| **TC4** | Escalation Metadata & Candidate Prefix Verification | 2 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- All commands must be run in the live mysql console.
