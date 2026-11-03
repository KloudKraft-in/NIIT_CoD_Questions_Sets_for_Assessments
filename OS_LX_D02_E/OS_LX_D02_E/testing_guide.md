# Testing Guide: OS_LX_D02_E (File Content Search & Text Filtering via Pipeline Commands)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Search for all:** Search for all files ending with .conf under /opt/app_data/ and save their file paths to ~/found_configs.txt.
3. **Parse the provided:** Parse the provided sample application log /opt/app_data/server.log for lines matching 'CRITICAL' (case-insensitive).
4. **Sort the matching:** Sort the matching lines alphabetically, count the unique critical errors, and write the count and sorted output to ~/critical_summary.txt.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and files, then display your score.
