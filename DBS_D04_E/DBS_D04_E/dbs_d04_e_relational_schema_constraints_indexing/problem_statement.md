# Database Lab : Relational Schema Architecture, Constraints & Indexing

Duration : 30 Min.

## Scenario

As a Database Engineer at NIIT, you are tasked with creating a normalized relational schema in PostgreSQL enforcing primary key, unique, and foreign key referential integrity constraints, and creating a secondary B-Tree index on foreign key columns.

## Input Details

The environment has been pre-configured with the following local database platform instances:

- **Database Host:** `localhost` (Ubuntu Linux VM)
- **PostgreSQL Service:** `localhost:5432` | DB: `postgres` | User: `postgres` | Password: `PostgresPassword123!` | CLI: `psql`

## Username & Naming Conventions

Your candidate prefix is: **`<prefix>`** (e.g. `student-exam123`).

Resource naming:
- **Customers Table:** `<prefix>_customers`
- **Orders Table:** `<prefix>_orders`
- **Foreign Key Index:** `idx_<prefix>_orders_cust`

## Task Objectives

Perform the following relational DDL steps directly in PostgreSQL using `psql`:

### 1. Create Customers Table
- Create table `<prefix>_customers` with columns:
  - `id SERIAL PRIMARY KEY`
  - `email VARCHAR(100) UNIQUE NOT NULL`
  - `full_name VARCHAR(100) NOT NULL`
  - `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`

### 2. Create Orders Table with Foreign Key
- Create table `<prefix>_orders` with columns:
  - `order_id SERIAL PRIMARY KEY`
  - `customer_id INT NOT NULL REFERENCES <prefix>_customers(id)`
  - `amount NUMERIC(10,2) NOT NULL`
  - `order_status VARCHAR(20) DEFAULT 'PENDING'`

### 3. Create Secondary B-Tree Index
- Create a secondary B-Tree index named `idx_<prefix>_orders_cust` on `<prefix>_orders(customer_id)`.

### 4. Verify Constraints with Seed Data
- Insert a customer record, insert an order referencing that customer, and verify that foreign-key integrity prevents inserting an order with a non-existent `customer_id`.

## Verification

Once you have created the tables and index, run the verification script:
```bash
python run.py
```
The verification system inspects `information_schema` and `pg_indexes` on `localhost:5432`.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Primary Key & Unique Constraint Definitions (<prefix>_customers) | 4 Marks |
| **TC2** | Foreign Key Referential Integrity (<prefix>_orders -> customers) | 3 Marks |
| **TC3** | B-Tree Index Creation (idx_<prefix>_orders_cust on customer_id) | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- Constraints must be enforceable in PostgreSQL catalog.
- Replace `<prefix>` with your lowercase candidate prefix.
