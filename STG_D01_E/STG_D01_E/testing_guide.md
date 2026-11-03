# Testing Guide: STG_D01_E (Block, File & Object Storage Classification & Service Mapping)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate commands or create the JSON mapping file in the terminal to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Ubuntu VM environment under `/home/ubuntu`.
2. **Workload Analysis:** Review the requirements for transactional database, concurrent shared media, and archival audit logs.
3. **Artifact Generation:** Create `~/storage_mapping.json` defining the storage models (Block, File, Object), protocols (iSCSI/NVMe, NFS/SMB, HTTPS/REST), and cloud equivalents (AWS, Azure, GCP).

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local VM environment, home directory structure, and `storage_mapping.json` file, then display your score.
