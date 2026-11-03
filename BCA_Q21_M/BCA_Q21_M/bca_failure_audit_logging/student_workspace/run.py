import subprocess
import sys
import os

def ensure_environment():
    ws = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(ws, "outage_trace.log")
    setup_script = os.path.join(ws, "setup_git.py")
    if os.path.exists(setup_script):
        subprocess.run([sys.executable, setup_script], cwd=ws, capture_output=True)

def main():
    ensure_environment()
    print("[SYSTEM] Running local tests...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.normpath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))
    if not os.path.exists(driver_path):
        print(f"[ERROR] Driver not found at: {driver_path}")
        sys.exit(1)
    
    result = subprocess.run([sys.executable, driver_path], capture_output=False, text=True)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
