import subprocess
import sys
import os

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.normpath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))
    subprocess.run([sys.executable, driver_path], capture_output=False)

if __name__ == "__main__":
    main()
