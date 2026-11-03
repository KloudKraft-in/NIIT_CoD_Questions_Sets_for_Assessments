# Storage Lab: SMB/CIFS Network Share Mount with Secure Credentials File

Duration : 30 Min.

## Scenario
A Linux application server needs to read reporting files from a Windows/Azure Files SMB share (`//smbserver.corp.local/finance`). Storing plaintext passwords in `/etc/fstab` is prohibited by corporate security policy. The administrator must inspect `cifs_mount_setup.log`, create a secured credentials file `/etc/cifs_credentials/smb_finance.cred` with permission `0600`, configure the CIFS mount in `/etc/fstab` using `credentials=` and `vers=3.0`, test file access, and record the configuration metrics in `cifs_mount_report.json`.

## Task Objectives

Perform the following secure SMB/CIFS share mount tasks:

> **Pre-Staged Files in `student_workspace/`:**
> - **`cifs_mount_setup.log`**: Raw system execution log documenting credentials configuration, permission hardening, fstab entry, and mount verification traces.
> - **`cifs_mount_report.json`**: Starter SMB/CIFS mount configuration report with `TODO_*` placeholders.

1. Review `cifs_mount_setup.log` and verify the secure credentials file for service account `svc_fin_app` with password `SecretPass#2026` at `/etc/cifs_credentials/smb_finance.cred`.
2. Restrict the permissions of the credentials file to `0600` to prevent unauthorized access by unprivileged users.
3. Configure a persistent CIFS mount for `//smbserver.corp.local/finance` to `/mnt/finance_share` in `/etc/fstab` using the credentials file and modern SMB protocol negotiation (`vers=3.0`).
4. Mount the share, verify via filesystem inspection that the type is correctly reported, and confirm read access.
5. Record your credentials path, permissions, mount options, and verification results in `cifs_mount_report.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Review the pre-staged `cifs_mount_setup.log` to inspect share parameters, credentials configuration, and permissions.
3. Update `cifs_mount_report.json` inside the `student_workspace/` directory, replacing all `TODO_*` placeholders with your verified configuration values.
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
| **TC1** | Credentials security: credentials file created with strict 0600 permissions and valid username/password format | 4 Marks |
| **TC2** | fstab configuration: CIFS entry uses credentials= parameter and modern protocol version vers=3.0 | 3 Marks |
| **TC3** | Share reachability: successful mount to /mnt/finance_share verified via mount and df output | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
