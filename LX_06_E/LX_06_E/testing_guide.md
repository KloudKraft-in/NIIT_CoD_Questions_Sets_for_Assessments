# Testing Guide: LX_09_E (Linux System Specification Reporting and Search)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **System Report:** Check the disk usage stats (`df -h`) and memory usage stats (`free`) and save the output in `/home/ubuntu/spec_report.txt` (e.g. `df -h > /home/ubuntu/spec_report.txt` and `free >> /home/ubuntu/spec_report.txt`).
3. **Log Search:** Search `/etc/resolv.conf` for the word `nameserver` and redirect the matches to `/home/ubuntu/search_results.txt` (e.g. `grep "nameserver" /etc/resolv.conf > /home/ubuntu/search_results.txt`).

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and files, then display your score.
