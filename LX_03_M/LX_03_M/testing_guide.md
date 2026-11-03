# Testing Guide: AWS_LX_06_M (Linux Network Troubleshooting & Archiving - Local VM)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Network Connectivity:** Test external network connectivity by sending exactly 4 ICMP ping packets to `google.com` and save the entire output to `/home/ubuntu/ping_results.txt`.
2. **Port Diagnostics:** Identify all actively listening TCP and UDP network ports on the instance (using `ss -tuln` or `netstat -tuln`) and save the output to `/home/ubuntu/open_ports.txt`.
3. **File Compression:** Create a dummy log file named `dummy_app.log` in `/home/ubuntu` and compress it into a gzip tarball archive named `app_archive.tar.gz` located in `/home/ubuntu`.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local connectivity log, open ports snapshot, and compressed tarball, then display your score.
