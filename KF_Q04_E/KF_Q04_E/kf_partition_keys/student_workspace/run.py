import subprocess
import sys
import os

def main():
    print("[SYSTEM] Initializing Kafka Task Verification...", flush=True)
    
    # Path to the driver.py located in the sibling secret_tests folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.normpath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))
    
    if not os.path.exists(driver_path):
        print(f"[ERROR] Evaluation engine not found at: {driver_path}", flush=True)
        sys.exit(1)
        
    # Execute the driver
    try:
        result = subprocess.run([sys.executable, driver_path], check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"[ERROR] Failed to run tests: {e}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
