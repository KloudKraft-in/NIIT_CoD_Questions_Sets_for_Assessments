# Testing Guide: OS_LX_D03_E (System State & Resource Utilization Inspection)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Capture system load:** Capture system load averages using uptime and append the output to ~/system_health.txt.
3. **Identify the top:** Identify the top 5 memory-consuming processes using ps aux sorted by memory and append the process list to ~/system_health.txt.
4. **Record human-readable disk:** Record human-readable disk utilization (df -hT) and memory stats in megabytes (free -m) into ~/system_health.txt.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and files, then display your score.
