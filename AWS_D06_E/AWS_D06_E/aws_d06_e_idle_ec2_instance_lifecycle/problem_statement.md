# AWS Lab: Idle EC2 Instance Lifecycle Management — Stop vs Terminate

Duration : 30 Min.

## Scenario
An oversized r5.2xlarge EC2 instance has been left running idle for two weeks in a sandbox account, accruing ongoing compute costs. The project owner wants compute billing to stop immediately, but all installed packages and configuration files must be preserved for future testing. The engineer must explain the financial and data retention differences between 'Stop' and 'Terminate', and execute the safe state transition.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon EC2 Compute Lifecycle
- **Target Instance ID:** `i-0192837465abc` (r5.2xlarge idle)
- **Lifecycle States:** Stopped (EC2 compute billed 0, EBS storage preserved) vs Terminated (destroyed)

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Query instance status using aws ec2 describe-instance-status for instance i-0192837465abc.
2. Compare cost implications of Stopped state (compute charges halt, EBS storage persists) vs Terminate (instance destroyed).
3. Formulate the CLI command aws ec2 stop-instances to halt compute charges safely, saving script to ~/stop_idle_instance.sh.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Status verification: correctly inspect instance state via EC2 CLI | 4 Marks |
| **TC2** | Billing trade-off: clearly explain why Stop preserves EBS while stopping EC2 compute hours | 3 Marks |
| **TC3** | Execution script: stop_idle_instance.sh contains valid CLI syntax with target instance ID | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
