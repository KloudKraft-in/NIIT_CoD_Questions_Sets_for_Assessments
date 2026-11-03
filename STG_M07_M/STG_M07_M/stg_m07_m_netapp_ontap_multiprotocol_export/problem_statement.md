# Storage Lab: NetApp ONTAP Multi-Protocol Export Failure & Access Policy Lockdown

Duration : 90 Min.

## Scenario
A Kubernetes worker cluster loses access to shared persistent volumes served from a NetApp ONTAP Storage Virtual Machine (SVM). Pods attempting to mount the NFS shares enter 'ContainerCreating' or 'CrashLoopBackOff' with 'mount.nfs: access denied by server while mounting'. An export policy was recently updated by security automation. The engineer must analyze the NetApp export policy rules (simulated CLI/REST config), detect client match CIDR errors, resolve root squashing / superuser security restrictions, verify junction path accessibility, and restore cluster connectivity.

## Task Objectives

Perform the following NetApp ONTAP multi-protocol export policy triage tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`netapp_incident.log`**: Incident log showing cluster mount errors, junction path status, SVM export policy rules, subnet diagnostics, and remediation output.
> - **`netapp_export_rca.json`**: Starter RCA report with `TODO_*` placeholders.

1. Inspect `netapp_incident.log` to identify the export policy rule defect preventing Kubernetes nodes from mounting storage.
2. Investigate superuser security and root squashing settings affecting volume initialization.
3. Formulate the corrected NetApp ONTAP CLI modification command to restore cluster connectivity.
4. Document your root cause analysis and policy governance controls in `netapp_export_rca.json`.

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
| **TC1** | Junction path validation: confirm volume junction path /vol_k8s_data is active in the SVM root namespace | 2 Marks |
| **TC2** | Client-match CIDR triage: correctly identify the subnet mismatch between worker nodes and export rule | 3 Marks |
| **TC3** | Superuser / Root Squash analysis: explain why 'superuser none' blocks kubelet volume initialization | 3 Marks |
| **TC4** | ONTAP command formulation: accurately construct the complete vserver export-policy rule modify command | 3 Marks |
| **TC5** | Access protocol verification: ensure rule permits both NFSv3 and NFSv4 protocol negotiations | 2 Marks |
| **TC6** | Client mount execution: test_mount.sh executes successfully and mounts the export without permission denied | 3 Marks |
| **TC7** | RCA completeness: netapp_export_rca.json provides detailed technical root cause and change-audit trail | 2 Marks |
| **TC8** | Prevention controls: define policy automated validation checks before applying future NetApp export rule changes | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
