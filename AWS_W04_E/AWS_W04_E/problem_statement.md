# AWS Lab: S3 Lifecycle Rule Configuration & Tiering Optimization

Duration : 30 Min.

## Scenario
An enterprise S3 bucket stores 100 TB of application logs in S3 Standard, resulting in high monthly storage charges. Analysis shows that logs are rarely accessed after 30 days and never accessed after 90 days, but must be retained for 365 days for regulatory compliance. The engineer must author an S3 Lifecycle configuration transitioning objects to Standard-IA at 30 days, Glacier at 90 days, and expiring them at 365 days.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon S3 Storage Class Management
- **Tiering Schedule:** Standard-IA at 30 days, Glacier Flexible at 90 days, Expire at 365 days
- **Rule Status:** `Enabled`

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Analyze log access frequency and retention requirements.
2. Apply and attach least-privilege IAM policy directly in AWS IAM
3. Define Transition rules: Standard-IA at 30 days, Glacier Flexible at 90 days, and Expiration at 365 days.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Lifecycle policy authoring: JSON document conforms to S3 Lifecycle schema | 4 Marks |
| **TC2** | Storage class transitions: transitions specify correct days and storage class constants | 3 Marks |
| **TC3** | Expiration rule: expiration action correctly configured for 365 days | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
