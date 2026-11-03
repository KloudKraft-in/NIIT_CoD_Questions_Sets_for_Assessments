# Testing Guide: OS_LX_D01_E (Linux Directory Navigation & System Path Hierarchy Setup)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Directory hierarchy creation:** Create nested directories `~/app_env/config`, `~/app_env/logs`, and `~/app_env/.secret_keys`.
3. **File placement:** Create empty files `~/app_env/config/app.conf` and `~/app_env/.secret_keys/auth.key`.
4. **Verification script:** Create `path_check.sh` that outputs the absolute path of `app.conf` and counts hidden files in `~/app_env/`.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and files, then display your score.
