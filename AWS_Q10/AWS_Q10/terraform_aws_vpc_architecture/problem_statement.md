# DevOps Lab: Terraform Infrastructure as Code: Provisioning an AWS VPC

**Difficulty Level:** Easy to Medium  
**Duration:** 60 Minutes

## Scenario

A cloud engineer needs to set up the foundational networking for a new AWS cloud environment using Infrastructure as Code. Creating networks manually in the AWS Console is prone to human error and difficult to duplicate across regions. To establish a clean, repeatable practice, the learner will write a simple Terraform configuration to create an AWS Virtual Private Cloud (VPC) with one public subnet and an Internet Gateway attached.

## Requirements

The learner must:

- Access the provided environment with Terraform installed and AWS credentials configured.
- Create a simple Terraform configuration (`main.tf`) that provisions:
  - An AWS VPC (`aws_vpc`) named `my-simple-vpc` with CIDR block `10.0.0.0/16`
  - A Public Subnet (`aws_subnet`) with CIDR block `10.0.1.0/24`
  - An Internet Gateway (`aws_internet_gateway`) attached to the VPC
  - A Public Route Table (`aws_route_table`) with a default route (`0.0.0.0/0`) targeting the Internet Gateway
  - A Route Table Association (`aws_route_table_association`) linking the Public Subnet to the Route Table
- Run `terraform init`, `terraform validate`, and `terraform apply -auto-approve` to create the resources in AWS.
- Generate a simple evaluation report file recording the Terraform validation and VPC creation status.

## Expected Workflow

```text
Write Terraform Config (main.tf)
      ↓
Terraform Init (terraform init)
      ↓
Validate Syntax (terraform validate)
      ↓
Apply Configuration (terraform apply)
      ↓
Verify AWS VPC & Subnet Created
      ↓
Evaluation Report Generation
```

## Sample Evaluation Report

Your environment should generate a report similar to the following:

```text
TF_INIT=SUCCESS
TF_VALIDATE=SUCCESS
VPC_NAME=my-simple-vpc
VPC_CIDR=10.0.0.0/16
SUBNET_CIDR=10.0.1.0/24
IGW_ATTACHED=true
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 14:30:15 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                         | Description                      |
| ----------------------------------- | -------------------------------- |
| **Terraform Configuration**   | `main.tf` with AWS networking    |
| **Active AWS VPC**            | Verified live AWS VPC instance   |
| **Subnet & IGW Mapping**      | Configured public networking     |
| **Evaluation Report File**    | Structured Terraform apply logs  |

## Technology Stack

| Technology                | Purpose                 |
| ------------------------- | ----------------------- |
| **Terraform**       | Infrastructure as Code  |
| **AWS VPC**         | Cloud Networking        |
| **HCL**             | HashiCorp Config Lang   |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case     | Requirement                            | Validation                                                | Marks    |
| ------------- | -------------------------------------- | --------------------------------------------------------- | -------- |
| **TC1** | **Terraform Initialization Check**| `terraform init` & `terraform validate` pass successfully | 10 Marks |
| **TC2** | **AWS VPC & Subnet Creation**    | VPC & Public Subnet exist in AWS with correct CIDRs       | 10 Marks |
| **TC3** | **Internet Gateway Attachment**  | Internet Gateway attached & Route Table associated        | 10 Marks |

**Total Score: 30 Marks**
