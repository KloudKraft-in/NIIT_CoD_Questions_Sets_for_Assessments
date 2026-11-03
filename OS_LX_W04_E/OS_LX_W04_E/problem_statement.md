# Linux Lab: RHEL Package Management, Repositories & Dependency Inspection (Local VM)

Duration : 30 Min.

## Scenario

An application installation on RHEL fails due to a missing runtime library. You must query configured package repositories, inspect package metadata and dependencies using dnf/rpm, enable or verify repositories, and verify clean package installation without broken dependencies.

## Task Objectives

Perform the following actions on your local Linux system:

### 1. Repository Audit and Identification

- Inspect active package repositories using `dnf repolist` (or equivalent package repository query).
- Save the active repository list and enabled repository IDs to `~/active_repos.txt`.

### 2. Package Metadata and Dependency Inspection

- Query package metadata for packages `nginx` and `jq` using `dnf info`.
- Ensure version, release, architecture, and size information are captured.
- Save the queried package details to `~/package_info.txt`.

### 3. Non-Interactive Package Installation and Verification

- Install the package `jq` non-interactively with zero unresolved dependencies (e.g., `sudo dnf install -y jq` or `sudo apt-get install -y jq`).
- Verify that the `jq` executable binary is installed and accessible in `PATH` (using `which jq`).
- Confirm the package's installed state using `rpm -q jq` (or `dpkg -s jq`).
- *(Optional fallback)*: You may also record installation verification details in `~/jq_installed.txt`.

> [!NOTE]
> **Pre-installed Package Notice**: If the `jq` package is already pre-installed on your VM environment, test cases TC3 and TC4 will show as PASSED initially. To test and verify the complete failure and installation lifecycle from scratch, you can first uninstall the prerequisite package (`sudo dnf remove -y jq` or `sudo apt-get remove -y jq`), run the verification to observe TC3 and TC4 fail, and then perform the clean non-interactive installation and verification to pass them.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Repository audit: dnf repolist correctly lists all enabled RHEL repository IDs | 2 Marks |
| **TC2** | Package metadata query: dnf info accurately extracts version and release details | 3 Marks |
| **TC3** | Package installation: jq package installed successfully with zero unresolved dependencies | 3 Marks |
| **TC4** | Verification check: rpm -q confirms installed state and executable binary is located in PATH | 2 Marks |

**Total Score: 10 Marks**
