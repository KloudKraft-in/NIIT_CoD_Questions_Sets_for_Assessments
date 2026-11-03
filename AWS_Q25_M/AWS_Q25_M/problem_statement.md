# DevOps Lab: AWS RDS MySQL Secure Database Provisioning

Duration : 90 Min.

## Scenario

As a DevOps engineer at Niit, you are tasked with provisioning a secure database backend. Your objective is to create a highly secure and cost-efficient MySQL database instance on AWS RDS for a new retail web application. To optimize costs and comply with security audits, the database must use the minimum cost tier, have storage autoscaling disabled, and be completely hidden from the public internet.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create RDS DB Instance

- **Engine:** MySQL (compatible version `8.0` - e.g. `8.0.35`)
- **Instance Identifier:** `retail-mysql-db-<your-labskraft-username>` (replace `<your-labskraft-username>` with your actual platform username in lowercase, e.g. `retail-mysql-db-labs-kraft-demo106`)

### 2. Configure DB Instance Details

- **Instance Class:** `db.t3.micro`
- **Storage:** `20 GiB` Allocated Storage (General Purpose SSD - `gp2` or `gp3`)
- **Publicly Accessible:** Set to **No** (disable public IP assignment)

### 3. Initialize Default Database

- **Initial Database Name:** Specify `retaildb` during database creation.

### 4. Configure Security Group

- **Access Rule:** Associate a Security Group with the RDS instance that explicitly allows inbound TCP traffic on port `3306` (standard MySQL port).

### 5. Disable Storage Autoscaling

- **Autoscaling:** Disable Storage Autoscaling (ensure the maximum storage threshold is disabled or set to `20` GiB).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                                           | Marks   |
| ------------- | ------------------------------------------------------------------------------------- | ------- |
| **TC1** | AWS Environment active and validated                                                  | 0 Marks |
| **TC2** | DB Instance exists with identifier`retail-mysql-db-<username>` and MySQL 8.0 engine | 4 Marks |
| **TC3** | DB Instance class is`db.t3.micro`, storage is 20 GiB, and public access is disabled | 4 Marks |
| **TC4** | Default database`retaildb` is created inside the instance                           | 4 Marks |
| **TC5** | Attached Security Group allows inbound TCP traffic on port 3306                       | 4 Marks |
| **TC6** | Storage autoscaling is disabled                                                       | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the DB instance name is exactly `retail-mysql-db-<your-labskraft-username>`.
- The database engine version must be compatible with MySQL 8.0.
- The security group must allow inbound traffic on port 3306.
