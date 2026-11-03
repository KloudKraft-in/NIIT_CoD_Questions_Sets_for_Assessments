# AWS Lab: Cloud Service Model Classification & Shared Responsibility Boundary

Duration : 30 Min.

## Scenario
An enterprise migration plan mistakenly designates AWS RDS PostgreSQL as IaaS, asserting that the internal infrastructure team is responsible for patching the guest Linux operating system. The cloud engineer must verify the guest OS access model for RDS, clarify the shared responsibility boundary, and generate a service classification document.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon Web Services (AWS)
- **Managed Database Engine:** Amazon RDS for PostgreSQL
- **Compute Engine:** Amazon EC2 (Elastic Compute Cloud)
- **Access Boundary:** No OS/root SSH access on RDS; Full guest-OS root access on EC2

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Inspect AWS RDS database configuration and verify that no SSH/guest-OS shell is exposed.
2. Reclassify Amazon EC2 as IaaS and Amazon RDS as PaaS.
3. Configure and verify in the AWS environment  customer vs AWS patching responsibilities.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Service classification: accurately identify RDS as PaaS and EC2 as IaaS | 4 Marks |
| **TC2** | Responsibility mapping: map OS patching, hypervisor security, and data backup across the boundary | 3 Marks |
| **TC3** | JSON output: aws_shared_responsibility.json conforms to expected schema | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
