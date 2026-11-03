# AWS Lab: Online EBS Volume Expansion & OS Filesystem Growth

Duration : 60 Min.

## Scenario
A production EC2 Linux server's EBS root volume (/dev/nvme0n1) is at 98% capacity. The cloud administrator expanded the volume from 30 GB to 80 GB using the AWS CLI: 'aws ec2 modify-volume --volume-id vol-0123 --size 80'. However, 'df -h' inside the operating system still shows only 30 GB on the root partition. The engineer must use 'growpart' to extend partition 1 and 'resize2fs' / 'xfs_growfs' to expand the filesystem online with zero downtime.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon Elastic Block Store (EBS) & Linux OS
- **Block Device:** `/dev/nvme0n1` (expanded from 30 GB to 80 GB)
- **Partition & Filesystem:** Partition 1 (`/dev/nvme0n1p1`), filesystem online growth

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Inspect disk and partition geometry using lsblk.
2. Execute growpart /dev/nvme0n1 1 to extend the partition.
3. Execute the appropriate filesystem resize utility (resize2fs or xfs_growfs) based on filesystem type.
4. Verify with df -h that usable space reflects 80 GB, documenting execution in ~/ebs_resize.log.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Geometry inspection: identify disparity between 80 GB raw block device and 30 GB partition | 5 Marks |
| **TC2** | Partition extension: growpart successfully expands partition 1 without data corruption | 5 Marks |
| **TC3** | Online filesystem growth: filesystem successfully resized online without reboot | 5 Marks |
| **TC4** | Verification: df confirms 80 GB capacity and test file creation succeeds | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
