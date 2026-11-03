# AWS Lab: Cloud Operations War Room — Multi-Tier Incident Resolution & Capstone

Duration : 90 Min.

## Scenario
During a simulated production launch war room, an e-commerce platform suffers four cascading operational failures within 15 minutes: (1) An IAM Service Control Policy update inadvertently denies S3 bucket access, breaking image downloads, (2) The primary web instance's EBS volume hits 100% capacity, freezing sessions, (3) An overly aggressive security script removes port 443 from the public ALB Security Group, cutting off user traffic, and (4) The primary CloudWatch alarm failed to page the on-call team because its SNS topic had no confirmed subscribers. The lead cloud engineer must prioritize the incidents by business urgency, resolve each fault end-to-end, and author the official Post-Incident Review.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** AWS Cloud Operations War Room & Disaster Remediation
- **Cascading Failures:** (1) ALB Security Group missing 443, (2) EBS volume 100% full, (3) SCP explicit Deny on S3, (4) Unsubscribed SNS alarm
- **Urgency Prioritization:** Client Traffic (ALB SG) -> Disk Full -> Storage Access (SCP) -> Monitoring

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Review war room incident telemetry from /opt/aws_warroom/incident_payloads.json.
2. Prioritize incident triage order: Traffic Blackhole (ALB SG) -> Disk Full -> Storage Access (IAM SCP) -> Silent Alarm.
3. Restore ALB Security Group: authorize HTTPS port 443 from 0.0.0.0/0 immediately.
4. Resolve Disk Full: expand EBS volume online and grow filesystem.
5. Resolve IAM Access: trace and remove explicit Deny statement from the organizational SCP.
6. Rebuild CloudWatch Alarm: re-subscribe on-call ops endpoints to the SNS topic and validate test notification.
7. Produce the comprehensive executive Post-Incident Review document at ~/aws_warroom_pir.md.
8. Verify that all application synthetic tests pass end-to-end with 100% health.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Prioritization rationale: establish correct business impact triage sequence | 2 Marks |
| **TC2** | ALB ingress restoration: restore port 443 ingress on ALB security group restoring client traffic | 3 Marks |
| **TC3** | EBS capacity recovery: expand volume and filesystem online restoring disk headroom | 3 Marks |
| **TC4** | SCP remediation: isolate and remediate organizational SCP deny rule restoring S3 access | 3 Marks |
| **TC5** | Monitoring repair: configure SNS topic subscription and trigger end-to-end alarm test | 2 Marks |
| **TC6** | Synthetic verification: run end-to-end health probe validating all microservice endpoints return 200 OK | 3 Marks |
| **TC7** | PIR documentation: aws_warroom_pir.md includes timeline, root causes, MTTA, MTTR, and preventive actions | 2 Marks |
| **TC8** | Governance guardrails: propose automated IaC drift detection and approval controls | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
