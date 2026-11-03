import os
import sys
import subprocess

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    driver_path = os.path.abspath(os.path.join("..", "secret_tests", "driver.py"))
    
    if not os.path.exists(driver_path):
        print(f"Error: Driver not found at {driver_path}")
        sys.exit(1)
        
    subprocess.call([sys.executable, driver_path])
