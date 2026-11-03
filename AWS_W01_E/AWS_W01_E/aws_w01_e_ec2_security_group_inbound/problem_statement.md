# AWS Lab: EC2 Security Group Inbound Rule Hardening

Duration : 30 Min.

## Scenario
A security scan flags an EC2 Security Group 'sg-web-dev' because port 22 (SSH) is open to '0.0.0.0/0' (the entire public internet). Corporate security policy mandates that administrative SSH access must be restricted strictly to the corporate VPN gateway IP (203.0.113.50/32). The engineer must modify the security group rules to revoke the overly permissive rule and authorize the single source IP.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon VPC Security Groups
- **Security Group:** `sg-web-dev`
- **Vulnerable Port:** Port 22 (SSH) open to `0.0.0.0/0`
- **Authorized Source:** Corporate VPN CIDR `203.0.113.50/32`

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Inspect current security group rules in /opt/aws_sec/sg_rules.json.
2. Revoke the open inbound rule (Port 22 from 0.0.0.0/0).
3. Authorize the restricted inbound rule (Port 22 from 203.0.113.50/32), saving CLI commands to ~/harden_sg.sh.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Vulnerability detection: identify the insecure 0.0.0.0/0 SSH inbound rule | 3 Marks |
| **TC2** | Rule revocation: construct valid aws ec2 revoke-security-group-ingress command | 4 Marks |
| **TC3** | Rule authorization: construct valid aws ec2 authorize-security-group-ingress scoped to single IP | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
