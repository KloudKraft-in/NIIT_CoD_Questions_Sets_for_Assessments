# Storage Lab: Data Protection Strategy — Snapshot vs Backup vs Replication Rules

Duration : 30 Min.

## Scenario
A junior storage engineer is tasked with designing backup schedules for four distinct corporate systems: (1) an operational e-commerce database requiring 15-minute point-in-time recovery, (2) an ERP database needing ransomware-isolated immutable retention for 7 years, (3) a high-availability disaster recovery database requiring sub-minute failover across regions, and (4) a dev/test environment needing instantaneous snapshot rollbacks before deployments. The engineer must match each requirement to Snapshot, Backup, or Continuous Replication, explaining the trade-offs.

## Task Objectives

Perform the following data protection and DR strategy formulation tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`dr_requirements.json`**: Technical profiles for the 4 enterprise disaster recovery requirements.
> - **`data_protection_policy.json`**: Starter policy JSON template with `TODO_*` placeholders.

1. Review the enterprise disaster recovery requirements in `dr_requirements.json`.
2. Evaluate the technical trade-offs between point-in-time snapshots, independent backups, and real-time replication.
3. Assign the optimal data protection mechanism to each business workload.
4. Formulate appropriate RPO and RTO targets for each tier based on storage engine characteristics.
5. Record your policy decisions and technical rationales in `data_protection_policy.json`.

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
| **TC1** | Strategy alignment: accurate assignment of snapshot, backup, and replication mechanisms to the 4 business requirements | 4 Marks |
| **TC2** | RPO/RTO quantification: realistic RPO and RTO thresholds assigned based on storage engine technical characteristics | 3 Marks |
| **TC3** | JSON schema validation: data_protection_policy.json is well-formed with rationale and failure isolation explanations | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
