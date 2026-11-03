import os
import sys
import subprocess

def run_tests():
    # Local simple runner matching QO-420 format (using subprocess for path safety)
    driver_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "secret_tests", "driver.py"))
    if os.path.exists(driver_path):
        # subprocess.run handles paths with special characters (like '&') safely
        subprocess.run([sys.executable, driver_path])
    else:
        print(f"Driver not found at: {driver_path}")

if __name__ == "__main__":
    run_tests()
