# Storage Lab: Cross-Cloud Storage Architecture & Performance Tier Selection

Duration : 30 Min.

## Scenario
A cloud migration initiative requires matching four specific application workloads to the exact storage tier across AWS, Azure, and GCP: (1) MongoDB with 25,000 sustained IOPS, (2) Web frontend root volume needing 3,000 baseline IOPS, (3) Cold log retention requiring cheapest per-GB cost, and (4) High-throughput financial streaming log requiring 800 MB/s throughput. The engineer must evaluate cloud storage specification sheets and map each workload to the recommended volume type.

## Task Objectives

Perform the following cross-cloud storage tier selection tasks inside your `student_workspace` directory:

> **Pre-Staged Files in `student_workspace/`:**
> - **`workload_profiles.json`**: Technical performance profiles for 4 enterprise application workloads.
> - **`cloud_storage_tiers.json`**: Starter multi-cloud mapping template with `TODO_*` placeholders.

1. Review `workload_profiles.json` and evaluate the performance characteristics (IOPS, throughput, latency, and cost sensitivity).
2. Select the optimal native storage volume types across AWS, Azure, and GCP that satisfy each workload's technical requirements.
3. Complete the multi-cloud tier selections in `cloud_storage_tiers.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Execute the required storage management commands, volume operations, or configuration edits.
3. If configuration files, backup manifests, or diagnostic reports are required, save them inside the `student_workspace` directory.
4. Verify your storage configurations locally by executing:
   ```bash
   python run.py
   ```
5. Once verified, return to the platform dashboard and click **"Run Tests"** / **"Full Eval"** to evaluate your score!

## Validation
Once your storage tasks are executed, return to the platform dashboard and click the **"Run Tests"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | High-IOPS database mapping: correctly select AWS io2, Azure Ultra Disk, and GCP pd-extreme | 3 Marks |
| **TC2** | General purpose workload mapping: select AWS gp3, Azure Premium SSD, and GCP pd-balanced | 2 Marks |
| **TC3** | Throughput-optimized workload mapping: select AWS st1 / io2, Azure Premium SSD v2, and GCP pd-ssd | 3 Marks |
| **TC4** | Archive tier mapping: select appropriate deep cold object storage tiers across all 3 providers | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
