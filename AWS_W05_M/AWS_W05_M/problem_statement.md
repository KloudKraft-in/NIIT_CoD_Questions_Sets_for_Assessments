# AWS Lab: Auto Scaling Group Golden AMI Scaling Under Load Triage

Duration : 60 Min.

## Scenario
A web application managed by an Auto Scaling Group (ASG) is dropping client connections during a traffic surge because average CPU utilization is at 98%. The ASG is stuck at 2 instances (Min: 2, Max: 6, Desired: 2) because its CloudWatch scaling policy was misconfigured with an impossible metric threshold (CPU > 150%). The engineer must inspect the ASG configuration, correct the scaling policy to trigger scale-out when average CPU exceeds 70%, trigger the scale-out event, and verify that 2 new instances launch from the golden Launch Template.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** AWS Auto Scaling Groups (ASG) & CloudWatch
- **ASG Configuration:** `/opt/aws_asg/asg_config.json`
- **Capacity Constraints:** Min: 2, Max: 6, Desired: 2 -> Scale out to 4
- **Target Metric Threshold:** Average CPU Utilization > 70%

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Inspect ASG configuration and CloudWatch alarm in /opt/aws_asg/asg_config.json.
2. Identify the invalid CPU alarm threshold.
3. Update the target-tracking scaling policy to maintain 70% average CPU utilization.
4. Formulate the verification sequence showing ASG scaling from 2 to 4 instances and reaching InService state.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Alarm defect identification: detect invalid metric threshold preventing automated scale-out | 5 Marks |
| **TC2** | Policy correction: construct valid target tracking or step scaling policy with 70% threshold | 5 Marks |
| **TC3** | Capacity scaling: verify DesiredCapacity increases from 2 to 4 instances | 5 Marks |
| **TC4** | Health check verification: confirm new instances pass EC2 and ELB health checks | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
