# Storage Lab: Hybrid Cloud Storage Migration & RPO/RTO Data Protection Plan

Duration : 90 Min.

## Scenario
An enterprise is migrating 500 TB of multi-tiered on-premises data (Fibre Channel SAN LUNs, NetApp NAS CIFS/NFS shares, and tape backup archives) to a hybrid multi-cloud environment leveraging AWS, Azure, and GCP. The migration architect must define the target storage service mapping, design the continuous replication and cutover strategy, establish disaster recovery RPO/RTO SLAs, configure cloud storage lifecycle policies (hot to cool to immutable archive), and design Azure Arc monitoring for remaining on-prem storage assets.

## Task Objectives

Perform the following hybrid cloud storage migration and architecture blueprint tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`hybrid_migration_assessment.log`**: Architecture assessment log summarizing 500 TB multi-tier source inventory, workload IOPS, protocol requirements, retention mandates, sync tooling, and SLA matrices.
> - **`hybrid_storage_migration_blueprint.json`**: Starter architecture specification with `TODO_*` placeholders.

1. Review `hybrid_migration_assessment.log` to map on-premises SAN block LUNs, NAS file shares, and tape archives to cloud equivalents.
2. Formulate quantifiable RPO and RTO disaster recovery SLA targets across mission-critical, operational, and archive tiers.
3. Define automated time-based lifecycle transition rules and WORM immutability policies from high-performance tiers to cold archives.
4. Define cutover and delta synchronization strategies, Azure Arc hybrid monitoring integration, and produce the complete specification in `hybrid_storage_migration_blueprint.json`.

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
| **TC1** | Block workload mapping: comprehensive IOPS, throughput, and capacity sizing for SAN-to-cloud block migration | 3 Marks |
| **TC2** | File share mapping: protocol parity (NFSv3/v4, SMB3) and permission preservation (NTFS ACLs, POSIX) defined | 3 Marks |
| **TC3** | Archive & compliance mapping: immutable WORM retention and lifecycle policies formulated across cloud tiers | 3 Marks |
| **TC4** | Lifecycle transition rules: precise time-based tiering rules from hot to cool to archive configured | 2 Marks |
| **TC5** | RPO/RTO SLA framework: quantifiable RPO and RTO targets defined with justification per business tier | 3 Marks |
| **TC6** | Cutover & delta sync plan: phased synchronization methodology minimizing production cutover maintenance window | 2 Marks |
| **TC7** | Azure Arc hybrid monitoring: architectural design incorporating Azure Arc for unified on-prem/cloud visibility | 2 Marks |
| **TC8** | Blueprint validation: hybrid_storage_migration_blueprint.json conforms to standard architecture schema | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
