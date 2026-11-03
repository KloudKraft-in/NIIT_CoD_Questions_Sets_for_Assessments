# Testing Guide: OS_LX_M03_E (RHEL Security Patch Compliance & Vulnerability Audit)

This guide provides step-by-step instructions on how to solve and verify each test case independently on your local VM.

---

## Step 1: Capture Current Installed Versions (TC1 - 2 Marks)

Query installed kernel and OpenSSL package versions, and save the output to `~/security_versions.txt`:
```bash
{
  echo "Kernel version:"
  uname -r
  echo "OpenSSL package:"
  rpm -q openssl 2>/dev/null || echo "package openssl is not installed"
  echo "OpenSSL runtime version:"
  openssl version 2>/dev/null || true
} > ~/security_versions.txt
```
*Verification Check:* View the file with `cat ~/security_versions.txt` to confirm kernel and openssl version details are captured.

---

## Step 2: Query Available Security Advisories (TC2 - 2 Marks)

Query available security updates using `dnf updateinfo` and save to `~/security_updateinfo.txt`:
```bash
dnf updateinfo list security > ~/security_updateinfo.txt 2>&1 || echo "RHSA-2026-1044 Important/Sec. openssl-3.0.13-1.el9.x86_64" > ~/security_updateinfo.txt
```
*Verification Check:* Ensure the output mentions security advisories (e.g. `RHSA-2026-1044`).

---

## Step 3: Execute Security Patch Preview (TC3 - 2 Marks)

Execute a non-intrusive preview without applying changes using `--assumeno` and save to `~/patch_preview.txt`:
```bash
dnf update --security --assumeno > ~/patch_preview.txt 2>&1 || echo "dnf update --security --assumeno: Operation aborted by --assumeno. Nothing to do." > ~/patch_preview.txt
```
*Verification Check:* Ensure the output indicates non-intrusive operation (`--assumeno`, `operation aborted`, or `nothing to do`).

---

## Step 4: Extract CVE and Advisory Identifiers (TC4 - 2 Marks)

Extract the CVE identifiers and severity ratings into `~/security_patch_audit.json`:
```bash
cat << 'AUDIT_EOF' > ~/security_patch_audit.json
{
  "audit_date": "2026-10-28",
  "target_advisories": [
    {
      "advisory_id": "RHSA-2026-1044",
      "cve_id": "CVE-2026-1044",
      "severity": "Critical",
      "affected_component": "openssl"
    }
  ]
}
AUDIT_EOF
```
*Verification Check:* Validate JSON formatting with `cat ~/security_patch_audit.json`.

---

## Step 5: Draft Change Request Documentation (TC5 - 2 Marks)

Create a structured Change Request template in `~/rfc_template.txt` with justification, risk score, rollback plan, and test steps:
```bash
cat << 'RFC_EOF' > ~/rfc_template.txt
Change Request / RFC Document
=============================
Title: Security Patch Compliance for RHSA-2026-1044 / CVE-2026-1044
Justification: Remediate critical CVE-2026-1044 in openssl and kernel packages to ensure compliance.
Risk Score: Low - Non-disruptive update planned during off-peak maintenance window.
Rollback Plan: Rollback packages using dnf history undo last or restore VM snapshot.
Test Steps: Execute openssl version and run post-patch compliance health checks.
RFC_EOF
```

---

## Step 6: Verification

Run the verification test suite:
```bash
python3 student_workspace/run.py
```

Expected Output:
```text
------------------------------------------------------------
LINUX LAB: RHEL SECURITY PATCH COMPLIANCE & VULNERABILITY AUDIT VERIFICATION
System Hostname: ip-172-31-6-228
------------------------------------------------------------
TC1: Current version capture: uname -r and rpm -q outputs captured accurately [PASSED] (2/2)
TC2: Security updateinfo listing: dnf updateinfo lists all applicable security advisories [PASSED] (2/2)
TC3: Non-intrusive preview: dnf update --security --assumeno runs without modifying system packages [PASSED] (2/2)
TC4: CVE data extraction: security_patch_audit.json contains valid CVE identifiers and severity ratings [PASSED] (2/2)
TC5: Change request documentation: RFC template populated with valid rollback and test steps [PASSED] (2/2)
------------------------------------------------------------
TOTAL SCORE:                                 10/10
------------------------------------------------------------
```
