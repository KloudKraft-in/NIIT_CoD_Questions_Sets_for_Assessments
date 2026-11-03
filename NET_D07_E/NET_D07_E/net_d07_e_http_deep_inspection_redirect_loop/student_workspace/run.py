import subprocess
import sys
import os

def main():
    print("[SYSTEM] Initializing Network Troubleshooting Task Verification...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.normpath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))
    
    if not os.path.exists(driver_path):
        print(f"[ERROR] Verification engine not found at: {driver_path}")
        sys.exit(1)
        
    try:
        result = subprocess.run([sys.executable, driver_path] + sys.argv[1:], check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"[ERROR] Failed to run verification: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
