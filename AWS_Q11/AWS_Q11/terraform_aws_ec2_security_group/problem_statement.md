# DevOps Lab: Terraform Provisioning AWS EC2 with Security Group

**Difficulty Level:** Easy to Medium  
**Duration:** 60 Minutes

## Scenario

A system administrator needs to launch an Ubuntu Linux virtual machine on AWS with a basic firewall that allows SSH access. Launching servers manually through the AWS Console can lead to mismatched security rules or forgotten firewall settings. To automate server creation, the learner will use Terraform to create a Security Group opening port 22 (SSH) and port 80 (HTTP), and launch a `t2.micro` EC2 instance attached to it.

## Requirements

The learner must:

- Access the provided environment with Terraform installed and AWS credentials configured.
- Create a simple Terraform configuration (`main.tf`) that provisions:
  - An AWS Security Group (`aws_security_group`) named `my-web-sg`
  - An Ingress rule allowing SSH traffic (Port `22`) from any IP (`0.0.0.0/0`)
  - An Ingress rule allowing HTTP traffic (Port `80`) from any IP (`0.0.0.0/0`)
  - An Egress rule allowing all outbound traffic (`0.0.0.0/0`)
  - An AWS EC2 Instance (`aws_instance`) using an Ubuntu AMI
  - Instance type configured as `t2.micro`
  - The instance must be associated with the newly created `my-web-sg` security group
  - Add a resource tag: `Name = MyWebServer`
- Run `terraform init`, `terraform plan`, and `terraform apply -auto-approve` to create the server in AWS.
- Generate a simple evaluation report file recording the Terraform plan and EC2 creation status.

## Expected Workflow

```text
Write Terraform Config (main.tf)
      ↓
Terraform Init (terraform init)
      ↓
Generate Plan (terraform plan)
      ↓
Apply Configuration (terraform apply)
      ↓
Verify Security Group Rules & EC2 Running
      ↓
Evaluation Report Generation
```

## Sample Evaluation Report

Your environment should generate a report similar to the following:

```text
TF_INIT=SUCCESS
TF_PLAN=SUCCESS
SG_NAME=my-web-sg
INGRESS_22_OPEN=true
INGRESS_80_OPEN=true
EC2_INSTANCE_ID=i-0123456789abcdef0
EC2_STATE=running
EC2_INSTANCE_TYPE=t2.micro
TAG_NAME=MyWebServer
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 15:30:15 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                         | Description                      |
| ----------------------------------- | -------------------------------- |
| **Terraform Configuration**   | `main.tf` with EC2 & SG          |
| **Active AWS EC2 Instance**   | Verified running `t2.micro` VM   |
| **Custom Security Group**     | Verified firewall ingress rules  |
| **Evaluation Report File**    | Structured Terraform apply logs  |

## Technology Stack

| Technology                | Purpose                 |
| ------------------------- | ----------------------- |
| **Terraform**       | Infrastructure as Code  |
| **AWS EC2**         | Compute Infrastructure  |
| **AWS Security Groups**| Virtual Firewall Rules  |
| **HCL**             | HashiCorp Config Lang   |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case     | Requirement                            | Validation                                                | Marks    |
| ------------- | -------------------------------------- | --------------------------------------------------------- | -------- |
| **TC1** | **Terraform Plan Verification**  | `terraform init` & `terraform plan` pass successfully     | 10 Marks |
| **TC2** | **Security Group Ingress Check** | Security Group exists with Ports 22 and 80 open           | 10 Marks |
| **TC3** | **EC2 Instance State & Tag Check**| EC2 instance running as t2.micro with correct Name tag    | 10 Marks |

**Total Score: 30 Marks**
