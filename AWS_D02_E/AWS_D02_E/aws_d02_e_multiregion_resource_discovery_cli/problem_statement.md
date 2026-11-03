# AWS Lab: Multi-Region Resource Discovery & CLI Region Targeting

Duration : 30 Min.

## Scenario
An application developer cannot see their newly created EC2 instance in the AWS Management Console and assumes provisioning failed. In reality, the console defaulted to us-east-1 while the instance was created in ap-south-1. The engineer must use the AWS CLI to query instances across regions, locate the missing server, and update the developer's default AWS CLI profile to prevent duplicate provisioning.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon Web Services (AWS CLI)
- **Target Region:** `ap-south-1` (Asia Pacific - Mumbai)
- **Target Availability Zone:** `ap-south-1a`
- **Instance Name Tag:** `web-app-prod`

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Run aws ec2 describe-instances across regions to locate instance 'web-app-prod'.
2. Identify the target Region (ap-south-1) and Availability Zone (ap-south-1a).
3. Configure default region targeting in AWS CLI profile that configures AWS_DEFAULT_REGION properly.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Instance discovery: correctly query multiple regions to locate the hidden instance | 4 Marks |
| **TC2** | Topology identification: identify the exact Region and AZ housing the resource | 3 Marks |
| **TC3** | Configuration update: set_default_region.sh correctly sets the environment default | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
