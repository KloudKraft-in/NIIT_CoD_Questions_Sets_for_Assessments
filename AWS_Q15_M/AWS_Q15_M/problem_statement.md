# DevOps Lab: Terraform + AWS S3 Backend & DynamoDB State Locking

**Difficulty Level:** Medium  
**Duration:** 30 Minutes

## Scenario

Your DevOps team is managing AWS infrastructure using Terraform, and multiple engineers frequently run terraform apply at the same time. Recently, this caused state file corruption, leading to mismatched resources. As a DevOps engineer, you must design a Terraform solution that ensures safe concurrent access to the state file using DynamoDB locking and centralized state storage in an S3 backend.

## Task Objectives

Perform the following actions in the environment:

### 1. Configure S3 Backend
### 2. Configure DynamoDB State Locking
### 3. Initialize Terraform

## Requirements

- **S3 Bucket Name:** `terraform-state-bucket-<your-labskraft-username>`
- Enable **Versioning** on the S3 bucket.
- **DynamoDB Table Name:** `terraform-lock-table-<your-labskraft-username>`
- **Partition Key:** `LockID` (String)

## Expected Workflow

Follow the task objectives sequentially to implement the architecture.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                    | Marks   |
| --------- | ---------------------------------------------- | ------- |
| **TC1**   | S3 Bucket Existence                            | 4 Marks |
| **TC2**   | S3 Bucket Versioning Enabled                   | 3 Marks |
| **TC3**   | S3 Bucket Encryption Enabled                   | 3 Marks |
| **TC4**   | DynamoDB Table Existence                       | 4 Marks |
| **TC5**   | DynamoDB Partition Key is LockID               | 3 Marks |
| **TC6**   | DynamoDB Table Billing Mode is PAY_PER_REQUEST | 3 Marks |

**Total Score: 20 Marks**

## Real-World Use Case

This solution simulates industry-grade workflows used by organizations to automate infrastructure deployments, validate configurations, and enable scalable hands-on lab evaluations.
