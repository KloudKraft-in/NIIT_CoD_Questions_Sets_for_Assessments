# Testing Guide: OS_LX_W01_E (File Permissions, Ownership & Sudoers Security Configuration)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Create a user:** Create a user group named appadmin and assign service account svc_deploy to it.
3. **Create directory /var/deploy_repo:** Create directory /var/deploy_repo with permissions 750 owned by svc_deploy:appadmin.
4. **Configure files inside:** Configure files inside /var/deploy_repo to default to 640 permissions.
5. **Add a sudoers:** Add a sudoers rule in /etc/sudoers.d/svc_deploy granting permission to restart the nginx service without a password.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and files, then display your score.
