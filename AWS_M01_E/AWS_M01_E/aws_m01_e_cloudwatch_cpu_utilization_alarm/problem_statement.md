# AWS Lab: CloudWatch CPU Utilization Alarm & SNS Notification Setup

Duration : 30 Min.

## Scenario
An unmonitored production EC2 instance experienced CPU saturation, causing an outage that was detected only after user complaints. The operations manager mandates that an automated CloudWatch alarm must be provisioned. The alarm must monitor CPUUtilization on instance i-0a1b2c3d4e5f, fire when CPU exceeds 80% for two consecutive 5-minute periods, and publish an alert to an SNS Topic 'arn:aws:sns:us-east-1:112233445566:ops-alerts'.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon CloudWatch & Amazon SNS
- **Target Instance:** `i-0a1b2c3d4e5f`
- **Metric:** `CPUUtilization`, Namespace: `AWS/EC2`, Threshold: `80%`
- **SNS Topic ARN:** `arn:aws:sns:us-east-1:112233445566:ops-alerts`

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Formulate the AWS CLI command aws cloudwatch put-metric-alarm with all required parameters.
2. Configure MetricName: CPUUtilization, Namespace: AWS/EC2, Threshold: 80, EvaluationPeriods: 2, Period: 300.
3. Attach AlarmActions referencing the target SNS Topic ARN.
4. Save the provisioning script to ~/create_cpu_alarm.sh.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Metric configuration: put-metric-alarm uses correct CPUUtilization metric and AWS/EC2 namespace | 3 Marks |
| **TC2** | Evaluation criteria: threshold set to 80 with 2 evaluation periods of 300 seconds | 2 Marks |
| **TC3** | Action integration: AlarmActions correctly attaches the SNS topic ARN | 3 Marks |
| **TC4** | Script validation: create_cpu_alarm.sh passes dry-run syntax verification | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
