# Testing Guide: AWS_LX_05_M (Linux File Operations & Security Permissions - Local VM)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Create Linux User:** Create a new user named `appuser` on the system.
3. **Setup Directory and Files:** Create a directory `/home/ubuntu/secure_data` containing blank `passwords.txt` and `config.ini` files.
4. **Configure Permissions:** Apply `400` (read-only by owner) on `passwords.txt` and `755` (read/write/execute by all) on `config.ini`.
5. **Update Ownership:** Change the owner of `config.ini` to `appuser`.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local user accounts, file permissions, and ownership, then display your score.
