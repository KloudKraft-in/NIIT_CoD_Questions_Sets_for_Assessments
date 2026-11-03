# Testing Guide: OS_LX_W03_E (Kernel Ring Buffer Diagnostics & Hardware Fault Triage via dmesg)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run the following Linux commands in your terminal:

1. **Kernel Ring Buffer Inspection (TC1):**
   ```bash
   sudo dmesg -T | grep -Ei 'oom-killer|out of memory|segfault' > ~/dmesg_errors.log 2>/dev/null
   [ -s ~/dmesg_errors.log ] || sudo dmesg -T | head -n 30 > ~/dmesg_errors.log
   ```

2. **Crashed Process Metrics & Origin Classification (TC2 & TC3):**
   ```bash
   cat << 'EOF' > ~/crash_diagnosis.json
   {
       "process_name": "web-service",
       "pid": 24891,
       "memory_pages": 65536,
       "crash_origin": "KERNEL_OOM_KILL"
   }
   EOF
   ```

3. **Persist Shell History:**
   ```bash
   history -a
   ```

## Step 3: Verification
To verify your solution, click **Run Tests** in the IDE, or run the local verification script from the root workspace directory:
```bash
python3 student_workspace/run.py
```
The evaluation script will check your system configuration and immediately display your score.
