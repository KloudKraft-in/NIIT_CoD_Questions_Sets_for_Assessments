import subprocess
import os

def setup_git_repo():
    ws = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["git", "init"], cwd=ws, capture_output=True)
    subprocess.run(["git", "config", "user.name", "dev_alice"], cwd=ws, capture_output=True)
    subprocess.run(["git", "config", "user.email", "alice@company.com"], cwd=ws, capture_output=True)
    
    outage_log = os.path.join(ws, "outage_trace.log")
    log_content = (
        "2026-08-06 09:55:00 [INFO] System initialized. Gateway listener active on port 8080.\n"
        "2026-08-06 09:58:12 [WARN] Correlation ID: tx-8891 - Incoming request /api/v1/transfer delayed.\n"
        "2026-08-06 09:58:42 [ERROR] Correlation ID: tx-8891 - Gateway timeout after 30 seconds waiting for downstream microservice response.\n"
        "2026-08-06 09:59:15 [CRITICAL] Database deadlock detected on transaction update_account_transfer (tx-8891). Lock wait timeout exceeded.\n"
        "2026-08-06 10:00:00 [CRITICAL] Primary Infrastructure & Integration failure. Database connection pool exhausted by commit 8c9e012. Exception: ConnectionTimeoutException at Pool.java:98\n"
    )
    with open(outage_log, "w", encoding="utf-8") as f:
        f.write(log_content)
    subprocess.run(["git", "add", "."], cwd=ws, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Hotfix: outage trace log baseline"], cwd=ws, capture_output=True)
    print("[SUCCESS] Outage RCA Git repo initialized!")

if __name__ == "__main__":
    setup_git_repo()
