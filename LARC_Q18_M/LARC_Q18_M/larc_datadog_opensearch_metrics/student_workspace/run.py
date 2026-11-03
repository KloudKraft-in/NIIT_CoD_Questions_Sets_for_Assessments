import subprocess
import sys
import os

def main():
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
