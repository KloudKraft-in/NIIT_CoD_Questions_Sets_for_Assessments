# Linux Lab: RHEL Security Patch Compliance & Vulnerability Audit (Local VM)

Duration : 30 Min.

## Scenario

A security advisory (RHSA-2026-1044) highlights a critical vulnerability in OpenSSL and the Linux kernel. As a compliance engineer, you must audit installed package versions against the CVE bulletin, perform a security patch preview without applying updates, and record the exact errata IDs.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Query installed kernel version

- Query installed kernel version using uname -r and openssl version using rpm -q openssl.

### 2. Query available security updates

- Query available security updates using dnf updateinfo list security.

### 3. Execute a security patch

- Execute a security patch preview without applying updates using dnf update --security --assumeno.

### 4. Extract all matching CVE

- Extract all matching CVE and Advisory IDs into ~/security_patch_audit.json.

### 5. Draft a structured Change

- Draft a structured Change Request template with justification, risk score, and rollback plan.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Current version capture: uname -r and rpm -q outputs captured accurately | 2 Marks |
| **TC2** | Security updateinfo listing: dnf updateinfo lists all applicable security advisories | 2 Marks |
| **TC3** | Non-intrusive preview: dnf update --security --assumeno runs without modifying system packages | 2 Marks |
| **TC4** | CVE data extraction: security_patch_audit.json contains valid CVE identifiers and severity ratings | 2 Marks |
| **TC5** | Change request documentation: RFC template populated with valid rollback and test steps | 2 Marks |

**Total Score: 10 Marks**
