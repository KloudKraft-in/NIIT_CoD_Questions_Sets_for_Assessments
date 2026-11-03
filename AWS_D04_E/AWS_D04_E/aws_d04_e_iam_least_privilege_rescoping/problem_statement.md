# AWS Lab: IAM Least Privilege Re-scoping for Operational Service Role

Duration : 30 Min.

## Scenario
A nighttime operations service role 'svc-nightops' currently has 'AdministratorAccess' attached. An internal audit flags this as a critical security finding. The role only requires permissions to describe EC2 instances, restart a specific tagged instance (Environment=NightlyTest), and stream CloudWatch logs. The engineer must author a scoped IAM policy adhering to the principle of least privilege.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** AWS Identity and Access Management (IAM)
- **Target Service Role:** `svc-nightops`
- **Required Permissions:** `ec2:DescribeInstances`, `ec2:RebootInstances` (scoped ARN), `logs:CreateLogStream`
- **Security Constraint:** Elimination of `Action: '*'` and `Resource: '*'`

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Inspect current permissions for svc-nightops in /opt/aws_iam/svc_nightops_policy.json.
2. Apply and attach least-privilege IAM policy directly in AWS IAM granting ec2:DescribeInstances, ec2:RebootInstances on specific ARN, and logs:CreateLogStream.
3. Ensure Action: '*' and Resource: '*' are completely eliminated.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Audit identification: recognize over-permissioned AdministratorAccess grant | 4 Marks |
| **TC2** | Policy authoring: write valid JSON IAM policy with scoped Actions and Resource ARNs | 3 Marks |
| **TC3** | Least privilege compliance: verify zero administrative wildcard permissions exist | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
