# Testing Guide: LX_08_E (Linux File Copying and Executable Permissions)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **File Copy:** Copy `/etc/hosts` to `/home/ubuntu/hosts_copy.txt`.
3. **Change Permissions:** Set permissions of `/home/ubuntu/hosts_copy.txt` to octal mode `755` (i.e. `chmod 755 /home/ubuntu/hosts_copy.txt`).

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and files, then display your score.
