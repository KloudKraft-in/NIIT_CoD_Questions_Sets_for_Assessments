# Testing Guide: OS_LX_W05_M (systemd Service Unit Management, Dependency Mapping & Failure Recovery)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Interrogate the failing:** Interrogate the failing service using systemctl status orders-api and journalctl -u orders-api -xe.
3. **Map the service:** Map the service dependency tree using systemctl list-dependencies orders-api to isolate the failed required unit.
4. **Correct the underlying:** Correct the underlying unit failure (missing socket directory or permission fault), start the prerequisite service, and restart orders-api.
5. **Enable orders-api to:** Enable orders-api to ensure persistent auto-start on system boot.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and files, then display your score.
