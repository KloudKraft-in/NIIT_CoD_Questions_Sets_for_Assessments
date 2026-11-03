# Database Lab : Replication Lag Telemetry Table & Monitoring Setup

Duration : 30 Min.

## Scenario

As a Database Operations Engineer at NIIT, reporting replicas are experiencing lag under burst write traffic. You must establish a replication telemetry audit database and table in MySQL, recording replication metrics, lag seconds, and escalation flags.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **MySQL Service:** `localhost:3306` | DB: `mysql` | User: `root` | Password: `MySQLPassword123!` | CLI: `mysql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **MySQL Monitoring Database:** `<prefix>_rep_monitor`
- **Replication Log Table:** `replica_telemetry`

## Task Objectives

Perform the following configuration steps directly via `mysql` CLI:

### 1. Create Monitoring Database
- In MySQL, create database `<prefix>_rep_monitor`.

### 2. Create Replica Telemetry Table
- Inside `<prefix>_rep_monitor`, create table `replica_telemetry` with columns:
  - `replica_id VARCHAR(50) PRIMARY KEY`
  - `channel_name VARCHAR(50) NOT NULL`
  - `seconds_behind_primary INT NOT NULL`
  - `replication_state VARCHAR(30) NOT NULL`
  - `escalation_required BOOLEAN NOT NULL`

### 3. Insert Telemetry Records
- Insert two simulated replica status entries:
  1. `('rep-analytics-01', 'main_channel', 2, 'STREAMING', FALSE)`
  2. `('rep-reporting-02', 'reporting_channel', 1840, 'STALLED', TRUE)`

## Verification

Once completed, run the verification script:
```bash
python run.py
```
The driver connects to MySQL on `localhost:3306` and queries `<prefix>_rep_monitor.replica_telemetry`.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | MySQL Database (<prefix>_rep_monitor) Creation | 4 Marks |
| **TC2** | Table (replica_telemetry) Schema & Column Constraints | 3 Marks |
| **TC3** | Replication Metric Data Population & Escalation Logic | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Replace `<prefix>` with your candidate prefix.
- All commands must be executed in the live MySQL console.
