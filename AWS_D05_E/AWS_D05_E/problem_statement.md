# AWS Lab: SCP Explicit-Deny Policy Precedence Investigation

Duration : 30 Min.

## Scenario
A developer assigned a role with 's3:GetObject' and 's3:ListBucket' (Allow) reports an 'AccessDenied' error when attempting to download an object from an S3 bucket in account 112233445566. An investigation reveals that the account belongs to an AWS Organizations Organizational Unit (OU) governed by an SCP containing an explicit Deny on S3 actions outside approved regions. The engineer must evaluate policy evaluation logic and diagnose the denial.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** AWS Organizations & IAM Policy Evaluation
- **Target Account:** `112233445566`
- **Evaluation Order:** Explicit Deny > Explicit Allow > Default Deny
- **Incident:** S3 GetObject blocked by Organizational Service Control Policy (SCP)

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Ingest IAM identity policy and Organization SCP policy from /opt/aws_iam/policy_evaluation.json.
2. Trace the AWS policy evaluation logic: Explicit Deny > Explicit Allow > Default Deny.
3. Output a policy diagnostic summary to ~/scp_precedence_analysis.json.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Policy parsing: successfully extract identity Allow and SCP Deny statements | 4 Marks |
| **TC2** | Precedence evaluation: correctly apply the explicit-deny override rule | 3 Marks |
| **TC3** | Analysis report: scp_precedence_analysis.json articulates why identity-level allow was overridden | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
