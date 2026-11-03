import subprocess
import sys
import os

def main():
    print("[SYSTEM] Initializing AWS Task Verification...", flush=True)
    
    # Path to the driver.py located in the sibling secret_tests folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.normpath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))
    
    if not os.path.exists(driver_path):
        print(f"[ERROR] Driver not found at: {driver_path}", flush=True)
        return

    # Execute the driver (which generates solution.json)
    cmd = [sys.executable, driver_path] + sys.argv[1:]
    result = subprocess.run(cmd, capture_output=False, text=True)

if __name__ == "__main__":
    main()
