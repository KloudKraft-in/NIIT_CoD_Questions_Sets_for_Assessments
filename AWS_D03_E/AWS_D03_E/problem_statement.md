# AWS Lab: EC2 Instance Family Sizing & Workload Profile Matching

Duration : 30 Min.

## Scenario
A development team requests an expensive memory-optimized instance (r6i.4xlarge) for a batch image transcoding worker. The worker's CPU utilization is at 100% while memory usage remains under 8%. The cloud engineer must evaluate instance type families (General Purpose, Compute Optimized, Memory Optimized, Storage Optimized) and recommend a right-sized Compute-Optimized (c6i) instance family.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon Web Services (EC2 Architecture)
- **Input Metrics Telemetry:** `/opt/aws_data/workload_metrics.json` (CPU: ~100%, RAM: <8%)
- **Evaluated Families:** T4g, M6i, C6i, R6i
- **Target Architecture Fit:** Compute-Optimized (C6i family)

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Ingest resource utilization telemetry from /opt/aws_data/workload_metrics.json.
2. Compare resource ratios (vCPU to Memory) across T4g, M6i, C6i, and R6i instance families.
3. Evaluate and verify target resource sizing in the AWS console

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Telemetry analysis: recognize high CPU and low memory profile from workload logs | 4 Marks |
| **TC2** | Family selection: select Compute Optimized (C-family) as the ideal architecture fit | 3 Marks |
| **TC3** | Recommendation report: JSON output contains exact instance type and cost delta | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
