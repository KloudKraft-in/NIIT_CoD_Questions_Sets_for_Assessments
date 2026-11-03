# AWS Lab: EBS Snapshot Creation & Volume Recovery Validation

Duration : 30 Min.

## Scenario
Before applying a major kernel upgrade to an EC2 instance, an administrator must create a point-in-time EBS snapshot of the data volume vol-0987654321fedcba. To validate that the backup is recoverable, the administrator must create a new test volume from the snapshot, attach it to a temporary instance, and verify file integrity.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon EBS Snapshot & Volume Management
- **Source Volume ID:** `vol-0987654321fedcba`
- **Target Availability Zone:** Same AZ as source volume

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Generate CLI command to create an EBS snapshot with description and tags.
2. Wait for snapshot status to transition to 'completed'.
3. Generate CLI command to create a new EBS volume in the same Availability Zone from the snapshot ID.
4. Output recovery procedure to ~/ebs_backup_recovery.sh.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Snapshot initiation: create-snapshot command specifies volume ID and descriptive tag | 3 Marks |
| **TC2** | Status polling: script implements wait command verifying completed snapshot state | 2 Marks |
| **TC3** | Volume restoration: create-volume command correctly references snapshot ID and target AZ | 3 Marks |
| **TC4** | Documentation: ebs_backup_recovery.sh provides clear restore verification workflow | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
