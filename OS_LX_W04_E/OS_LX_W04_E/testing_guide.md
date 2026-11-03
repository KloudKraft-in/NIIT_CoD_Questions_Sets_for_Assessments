# Testing Guide: OS_LX_W04_E (RHEL Package Management, Repositories & Dependency Inspection)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run the following Linux commands in your terminal:

1. **Repository Audit (TC1):**
   ```bash
   dnf repolist > ~/active_repos.txt 2>/dev/null || apt-cache policy > ~/active_repos.txt
   ```

2. **Package Metadata Query (TC2):**
   ```bash
   dnf info nginx jq > ~/package_info.txt 2>/dev/null || apt-cache show nginx jq > ~/package_info.txt
   ```

3. **Package Installation and Verification (TC3 & TC4):**
   > **Note on Pre-installed Packages**: In environments where `jq` is already pre-installed, TC3 and TC4 will show as PASSED initially. To test the full failure/pass lifecycle, you may first uninstall `jq`:
   > ```bash
   > sudo dnf remove -y jq 2>/dev/null || sudo apt-get remove -y jq
   > rm -f ~/jq_installed.txt
   > ```
   > Run tests to confirm TC3 & TC4 fail (0 Marks), then perform the clean non-interactive installation:
   ```bash
   sudo dnf install -y jq 2>/dev/null || (sudo apt-get update && sudo apt-get install -y jq)
   which jq > ~/jq_installed.txt 2>/dev/null || true
   rpm -q jq >> ~/jq_installed.txt 2>/dev/null || dpkg -s jq >> ~/jq_installed.txt 2>/dev/null || true
   ```

4. **Persist Shell History:**
   ```bash
   history -a
   ```

## Step 3: Verification
To verify your solution, click **Run Tests** in the IDE, or run the local verification script from the root workspace directory:
```bash
python3 student_workspace/run.py
```
The evaluation script will check your repository list, package metadata, and `jq` installation, immediately displaying your score:
```text
------------------------------------------------------------
LINUX LAB: RHEL PACKAGE MANAGEMENT, REPOSITORIES & DEPENDENCY INSPECTION VERIFICATION
System Hostname: <hostname>
------------------------------------------------------------
TC1: Repository audit: dnf repolist correctly lists all enabled RHEL repository IDs [PASSED] (2/2)
TC2: Package metadata query: dnf info accurately extracts version and release details [PASSED] (3/3)
TC3: Package installation: jq package installed successfully with zero unresolved dependencies [PASSED] (3/3)
TC4: Verification check: rpm -q confirms installed state and executable binary is located in PATH [PASSED] (2/2)
------------------------------------------------------------
TOTAL SCORE:                                 10/10
------------------------------------------------------------
```
