# AWS LAB : S3 Infrastructure Provisioning

Duration : 60 Min.

## Scenario

As a DevOps engineer at Niit, you are tasked with provisioning cloud infrastructure securely. Your objective is to create an S3 bucket in the AWS environment that adheres to the organization's security and regional policies.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create S3 Bucket

- **Bucket Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual Niit username, e.g. `labs-kraft-demo106`)
- **Region:** `eu-west-2` (Europe - London)

### 2. Configure Security (Public Access Block)

Ensure the bucket is secured by enabling the following **Public Access Block** settings:

- **Block public ACLs** (BlockPublicAcls)
- **Block public bucket policies** (BlockPublicPolicy)

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                           | Marks   |
| ------------- | ----------------------------------------------------- | ------- |
| **TC1** | Bucket Existence (`<username>-<exam_code>`) | 5 Marks |
| **TC2** | Public Access Blocked (ACLs & Policies)               | 5 Marks |
| **TC3** | Correct Region Selection (`eu-west-2`)              | 5 Marks |

**Total Score: 15 Marks**

## Important Notes

- Ensure the bucket name is exactly `<your-labskraft-username>-<your-exam-code>`.
- If the bucket exists but is in the wrong region, TC3 will fail.
- Both Public ACL and Public Policy blocks must be enabled for TC2 to pass.
