# AWS Lab: S3 Block Public Access Enforcement & Live 403 Verification

Duration : 30 Min.

## Scenario
A compliance audit detects that an S3 bucket 'acme-internal-financial-reports' has public read access enabled, exposing confidential spreadsheets. The cloud engineer must enable S3 Block Public Access at the bucket level (blocking public ACLs and public policies) and verify that unauthenticated anonymous GET requests return HTTP 403 Forbidden.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon Simple Storage Service (S3)
- **Bucket Name:** `acme-internal-financial-reports`
- **Public Access Block Settings:** BlockPublicAcls, IgnorePublicAcls, BlockPublicPolicy, RestrictPublicBuckets

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Inspect bucket permissions in /opt/aws_s3/bucket_policy.json.
2. Formulate the AWS CLI command to apply complete Block Public Access settings.
3. Execute a verification script testing that an anonymous curl request to the bucket returns HTTP 403.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Exposure detection: identify public read permissions in bucket ACL / policy | 4 Marks |
| **TC2** | Block Public Access configuration: construct valid put-public-access-block command enabling all 4 block settings | 3 Marks |
| **TC3** | 403 verification: verify anonymous HTTP GET returns 403 Forbidden | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
