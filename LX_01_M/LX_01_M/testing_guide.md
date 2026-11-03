# Testing Guide: AWS_LX_04_M (Linux File System & Directory Navigation - Local VM)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Create the directories:** Create the target folders `/home/ubuntu/app_navigation/config` and `/home/ubuntu/app_navigation/logs`.
3. **Create target files:** Create empty configuration and error files in the respective folders (`app.conf` inside `/home/ubuntu/app_navigation/config`, and `error.log` inside `/home/ubuntu/app_navigation/logs`).
4. **Backup configuration & Keyword search:** Copy `app.conf` to `/home/ubuntu/app_navigation/` and rename it to `app.conf.backup`. Find all files or content containing the keyword `"app"` inside `/home/ubuntu` and redirect/append the output to `/home/ubuntu/search_results_nav.txt`.
5. **Disk analysis:** Run the command to show human-readable file system disk usage and save the output directly to `/home/ubuntu/disk_usage_nav.txt`.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, `/home/ubuntu` directory structure, files, permissions, and logs, then display your score.
