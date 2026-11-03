# DevOps Lab: Serverless S3 Event Notifications

**Difficulty Level:** Medium  
**Duration:** 30 Minutes

## Scenario

A company stores important compliance documents in an S3 bucket. Whenever a new file is uploaded, the compliance team must be notified immediately by email. You are asked to design an automated solution using serverless services to ensure this workflow runs reliably and securely.

## Task Objectives

Perform the following actions in the environment:

### 1. Create S3 Bucket
### 2. Create SNS Topic with Email Subscription
### 3. Configure S3 Event Notification

## Requirements

- **S3 Bucket Name:** `compliance-docs-<your-labskraft-username>`
- **SNS Topic Name:** `compliance-alerts-<your-labskraft-username>`
- Configure SNS topic with an Email subscription.
- Configure S3 Event Notification to trigger the SNS topic for `s3:ObjectCreated:*` events.

## Expected Workflow

Follow the task objectives sequentially to implement the architecture.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                     | Marks   |
| --------- | ----------------------------------------------- | ------- |
| **TC1**   | S3 Bucket Existence                             | 4 Marks |
| **TC2**   | SNS Topic Existence                             | 3 Marks |
| **TC3**   | SNS Topic Email Subscription exists             | 3 Marks |
| **TC4**   | SNS Topic Policy allows S3 to publish           | 4 Marks |
| **TC5**   | S3 Bucket Event Notification configured to SNS  | 3 Marks |
| **TC6**   | S3 Event Notification filters for ObjectCreated | 3 Marks |

**Total Score: 20 Marks**

## Real-World Use Case

This solution simulates industry-grade workflows used by organizations to automate infrastructure deployments, validate configurations, and enable scalable hands-on lab evaluations.
