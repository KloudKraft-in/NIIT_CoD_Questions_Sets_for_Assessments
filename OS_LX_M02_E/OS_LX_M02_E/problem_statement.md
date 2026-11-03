# Linux Lab: Enterprise Support Bundle Generation via sosreport (Local VM)

Duration : 30 Min.

## Scenario

An enterprise operating system support case requires submitting a comprehensive diagnostic bundle to vendor engineering. You must execute Red Hat's sosreport utility non-interactively, specifying ticket case numbers, selecting relevant diagnostic plugins (kernel, memory, networking), and verifying the integrity of the generated tarball archive.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Run sosreport in non-interactive

- Run sosreport in non-interactive batch mode (--batch) supplying case ID 'CASE-88421'.

### 2. Scope plugins to include

- Scope plugins to include networking, systemd, memory, and kernel subsystems while obfuscating sensitive data.

### 3. Verify the generated tar.xz

- Verify the generated tar.xz support bundle archive in /var/tmp/.

### 4. Compute and save the

- Compute and save the sha256 checksum of the generated bundle into /var/tmp/sosreport-checksum.txt.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Batch execution: sosreport --batch completes without user prompts or interactive pauses | 3 Marks |
| **TC2** | Case tagging: bundle metadata correctly contains Case ID CASE-88421 | 2 Marks |
| **TC3** | Bundle archive generation: compressed .tar.xz archive created in /var/tmp/ | 3 Marks |
| **TC4** | Checksum verification: valid sha256 hash generated and matches bundle file | 2 Marks |

**Total Score: 10 Marks**
