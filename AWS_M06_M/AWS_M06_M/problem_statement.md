# AWS Lab: FinOps Cost Governance & Runaway Compute/Storage Triage

Duration : 90 Min.

## Scenario
A company's monthly AWS bill unexpectedly surged by 45% ($18,000 overrun), triggering a budget breach alert. The FinOps engineer is given a raw Cost Explorer JSON export and resource inventory across the account. The engineer must identify the three primary cost drivers: (1) 25 unattached, orphaned gp3 and io2 EBS volumes left behind after terminated test instances, (2) five oversized p3.8xlarge GPU instances running 24/7 with 0% GPU utilization, and (3) an S3 bucket with 150 TB of un-lifecycle-managed analytics dumps. The engineer must quantify the wastage and implement remediation scripts.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** AWS FinOps Cost Governance & Cost Explorer
- **Cost Report:** `/opt/aws_finops/cost_explorer_report.json` ($18,000 monthly overrun)
- **Cost Drivers:** (1) 25 unattached gp3/io2 EBS volumes, (2) 5 idle p3.8xlarge instances, (3) 150 TB un-lifecycle-managed S3 bucket

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Analyze Cost Explorer data from /opt/aws_finops/cost_explorer_report.json.
2. Identify unattached EBS volumes: query volumes where Status=available and calculate monthly idle cost.
3. Identify idle EC2 instances: correlate CPU/GPU utilization telemetry to flag oversized idle instances.
4. Identify unoptimized S3 storage: calculate cost savings from transitioning Standard to Glacier.
5. Apply and attach least-privilege IAM policy directly in AWS IAM that deletes unattached volumes older than 14 days.
6. Generate a formal FinOps executive report ~/finops_savings_plan.md detailing total identified monthly savings.
7. Implement an AWS Budget alert to notify the team when spend reaches 80% of forecasted monthly baseline.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Data ingestion: correctly parse Cost Explorer breakdown by service and usage type | 3 Marks |
| **TC2** | Orphaned storage isolation: identify all unattached EBS volumes and compute wasted monthly spend | 3 Marks |
| **TC3** | Idle compute detection: identify oversized p3 instances running idle via CloudWatch metric correlation | 3 Marks |
| **TC4** | S3 cost modeling: calculate exact financial savings achieved by applying Lifecycle transition rules | 3 Marks |
| **TC5** | Remediation script: finops_remediation.py safely targets orphaned resources with dry-run support | 3 Marks |
| **TC6** | Executive report: finops_savings_plan.md outlines immediate vs ongoing recurring savings | 3 Marks |
| **TC7** | Budget guardrail: configure AWS Budget alarm threshold and SNS notification payload | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
