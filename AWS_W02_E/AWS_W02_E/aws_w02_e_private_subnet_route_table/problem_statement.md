# AWS Lab: Private Subnet Route Table & NAT Gateway Egress Triage

Duration : 30 Min.

## Scenario
EC2 instances in a private application subnet (subnet-priv-01) cannot download security patches from public package repositories. An engineer suspects a networking misconfiguration. The route table associated with the private subnet is missing a default route (0.0.0.0/0) pointing to the NAT Gateway (nat-0a1b2c3d4e5f) located in the public subnet. The engineer must inspect the route table and add the missing default egress route.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon VPC Route Tables & NAT Gateways
- **Subnet:** `subnet-priv-01` (Private subnet)
- **Route Table ID:** `rtb-01234`
- **NAT Gateway ID:** `nat-0a1b2c3d4e5f` (Public subnet)

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Ingest VPC route table configuration from /opt/aws_net/route_table.json.
2. Diagnose why instances cannot reach external IP addresses (missing 0.0.0.0/0 destination).
3. Write an AWS CLI command to create the route: aws ec2 create-route --route-table-id rtb-01234 --destination-cidr-block 0.0.0.0/0 --nat-gateway-id nat-0a1b2c3d4e5f.
4. Output verification steps to ~/nat_route_fix.sh.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Route table inspection: parse route table entries and identify missing internet destination | 3 Marks |
| **TC2** | NAT target identification: locate the operational NAT Gateway ID in the public subnet | 2 Marks |
| **TC3** | Command creation: nat_route_fix.sh contains valid create-route CLI syntax | 3 Marks |
| **TC4** | Verification check: script includes route table describe command to verify active status | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
