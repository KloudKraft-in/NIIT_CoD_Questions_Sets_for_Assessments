import subprocess
import sys
import os

def main():
    print("[SYSTEM] Initializing Jenkins Parameterized Job Verification...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.normpath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))
    
    if not os.path.exists(driver_path):
        print(f"[ERROR] Driver not found at: {driver_path}")
        return
        
    try:
        user_args = [sys.argv[1]] if len(sys.argv) > 1 else []
        subprocess.run([sys.executable, driver_path] + user_args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Test driver execution failed with code {e.returncode}")
    except Exception as e:
        print(f"[ERROR] Could not start verification: {e}")

if __name__ == "__main__":
    main()
