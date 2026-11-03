# DevOps Lab: AWS EC2 (Windows DB Server) & Advanced Storage Management

Duration : 30 Min.

## Scenario

As a DevOps engineer at Niit, you need to configure a comprehensive Windows-based compute and storage solution for a database. Your task involves setting up a Windows Server EC2 instance, creating a high-performance EBS volume, attaching it, and initializing/formatting it for database storage using Windows Disk Management.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Windows Server)

- **Instance Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual Niit username, e.g. `labs-kraft-demo106`)
- **AMI (Operating System):** Microsoft Windows Server (e.g., 2022 Base)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. Create EBS Volume

- **Volume Size:** `20 GB`
- **Volume Type:** `io2` (Provisioned IOPS SSD) with 500 IOPS

### 3. Attach, Initialize, and Format the EBS Volume in Windows

- **Attach Volume:** Attach the created EBS volume to the Windows EC2 instance.
- **Initialization:** Bring the newly attached disk online and initialize it.
- **File System:** Format the attached volume with the `NTFS` filesystem.
- **Drive Letter/Mount:** Assign the volume the drive letter `F:`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                                                         | Marks   |
| --------- | ----------------------------------------------------------------------------------- | ------- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Windows, named `<username>-<exam_code>`)| 5 Marks |
| **TC2**   | EBS Volume Created (20 GB, `io2` with 500 IOPS)                                     | 5 Marks |
| **TC3**   | EBS Volume Attached to EC2, Formatted as `NTFS` and Assigned Drive Letter `F:`      | 5 Marks |

**Total Score: 15 Marks**

## Important Notes

- Ensure the instance name is exactly `<your-labskraft-username>-<your-exam-code>`.
- The instance must be a Windows Server machine of type `t2.micro`.
- You will need to connect to the instance (via RDP) to use Disk Management or PowerShell to initialize and format the disk.
