# Testing Guide: LX_11_M (Memory Log Rotation and Cron Telemetry - Local VM)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM under the `ubuntu` user (`/home/ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Create Telemetry Folder:** `mkdir -p /home/ubuntu/telemetry`
2. **Process Audit:** `ps aux --sort=-%mem | head -n 4 > /home/ubuntu/telemetry/memory_hogs.txt`
3. **Log Search:** `grep -iE "fail|critical" /var/log/dpkg.log | tail -n 15 > /home/ubuntu/telemetry/critical_events.log`
4. **Register Cron Job:** Add entry to `crontab -e`:
   `*/5 * * * * (date; uptime) >> /home/ubuntu/telemetry/cpu_load.log`

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 linux_cron_telemetry_local/student_workspace/run.py` from the root workspace directory.
- The evaluation script will check telemetry files, crontab entries, and process data, then display your score.
