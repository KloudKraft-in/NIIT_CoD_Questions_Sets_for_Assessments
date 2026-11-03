# AWS Lab: S3 Versioning Activation & Accidental Deletion Rollback

Duration : 30 Min.

## Scenario
A deployment script accidentally overwrote and deleted a critical application configuration file 'app-config.json' in an S3 bucket. Fortunately, S3 Versioning had been enabled. The engineer must inspect the bucket's object versions, locate the Delete Marker, remove the Delete Marker to restore the object, and retrieve the prior version.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon S3 Object Versioning
- **Target File:** `app-config.json`
- **Remediation Action:** Delete active Delete Marker to rollback to prior version

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Check bucket versioning status using aws s3api get-bucket-versioning.
2. List object versions and delete markers using aws s3api list-object-versions.
3. Delete the active Delete Marker to restore the latest non-deleted object version.
4. Verify that the restored object matches the original MD5 checksum, saving commands to ~/s3_version_recovery.sh.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Versioning query: verify bucket versioning configuration is active | 3 Marks |
| **TC2** | Version enumeration: list-object-versions identifies the specific Delete Marker version ID | 2 Marks |
| **TC3** | Object restoration: delete-object removes Delete Marker restoring the underlying version | 3 Marks |
| **TC4** | Checksum validation: verify restored object content matches expected baseline | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
