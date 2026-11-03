# Testing Guide: LX_07_E (Linux Working with Directories and File Operations)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Create the directory:** Create the target folder `/home/ubuntu/workspace`.
3. **Create target file:** Create an empty file `temp.txt` inside `/home/ubuntu/workspace`.
4. **File operations:** Move the file `temp.txt` from `/home/ubuntu/workspace` to `/home/ubuntu/` and rename it to `final.txt`.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and files, then display your score.
