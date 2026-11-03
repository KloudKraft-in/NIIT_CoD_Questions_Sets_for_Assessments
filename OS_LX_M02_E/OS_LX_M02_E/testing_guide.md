# Testing Guide: OS_LX_M02_E (Enterprise Support Bundle Generation via sosreport)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Run sosreport in:** Run sosreport in non-interactive batch mode (--batch) supplying case ID 'CASE-88421'.
3. **Scope plugins to:** Scope plugins to include networking, systemd, memory, and kernel subsystems while obfuscating sensitive data.
4. **Verify the generated:** Verify the generated tar.xz support bundle archive in /var/tmp/.
5. **Compute and save:** Compute and save the sha256 checksum of the generated bundle into /var/tmp/sosreport-checksum.txt.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and files, then display your score.
