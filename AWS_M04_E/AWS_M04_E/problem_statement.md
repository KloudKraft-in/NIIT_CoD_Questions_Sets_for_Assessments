# AWS Lab: EC2 Status Checks Sweep & Hardware Degradation Triage

Duration : 30 Min.

## Scenario
A routine monitoring sweep reports that EC2 instance i-0abcdef123456789 is failing status checks (StatusCheckFailed_System = 1, StatusCheckFailed_Instance = 0). The junior engineer attempts to reboot the instance from inside the OS, but the check continues to fail. The engineer must distinguish between a System Status check failure (underlying physical host issue) and an Instance Status check failure (guest OS crash), and apply the correct remediation: stopping and starting the instance to migrate it to a healthy physical host.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon EC2 CloudWatch Status Checks
- **Metrics:** `StatusCheckFailed_System` (Hardware/Host) vs `StatusCheckFailed_Instance` (Guest OS)
- **Host Degradation Remediation:** Stop and Start instance to migrate hardware host

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Query instance status check details using aws ec2 describe-instance-status.
2. Differentiate between StatusCheckFailed_System and StatusCheckFailed_Instance.
3. Explain why OS reboot fails to resolve hardware faults.
4. Execute stop-instances followed by start-instances to trigger hypervisor re-instantiation on new hardware.
5. Output findings to ~/status_check_triage.json.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Check parsing: correctly identify System status check failure vs Instance check | 2 Marks |
| **TC2** | Root cause explanation: articulate that System check failures represent AWS underlying hardware faults | 2 Marks |
| **TC3** | Remediation logic: explain why stop/start migrates the instance while in-guest reboot does not | 2 Marks |
| **TC4** | CLI sequence: construct valid stop-instances and start-instances workflow | 2 Marks |
| **TC5** | Post-check verification: verify both status checks return 'passed' | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
