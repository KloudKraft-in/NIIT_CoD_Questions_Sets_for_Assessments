# DevOps Lab: AWS EC2 (Ubuntu) & Storage Infrastructure Provisioning

Duration : 30 Min.

## Scenario

As a DevOps engineer at Niit, you are tasked with provisioning compute and storage infrastructure. Your objective is to create an Ubuntu Linux EC2 instance, provision an EBS volume, attach it to the instance, and mount the storage using standard Linux commands.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual Niit username, e.g. `labs-kraft-demo106`)
- **AMI (Operating System):** Ubuntu Server (e.g., 22.04 LTS)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. Create and Attach EBS Volume

- **Volume Size:** `10 GB`
- **Volume Type:** `gp3` (General Purpose SSD)
- **Attach Volume:** Attach the created EBS volume to the Ubuntu EC2 instance created in the previous step.

### 3. Mount the EBS Volume in Linux

- **File System:** Format the attached volume with the `ext4` filesystem.
- **Mount Point:** Mount the volume to the directory `/mnt/data-store`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                                                          | Marks   |
| --------- | ------------------------------------------------------------------------------------ | ------- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `<username>-<exam_code>`) | 5 Marks |
| **TC2**   | EBS Volume Created (10 GB, `gp3`) and Attached to EC2                                | 5 Marks |
| **TC3**   | EBS Volume Mounted at `/mnt/data-store` (`ext4`)                                     | 5 Marks |

**Total Score: 15 Marks**

## Important Notes

- Ensure the instance name is exactly `<your-labskraft-username>-<your-exam-code>`.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
- Ensure the EBS volume is mounted persistently so it survives a reboot (e.g., configured in `/etc/fstab`).
