import os
import sys

def run_tests():
    # Local simple runner that calls the driver in secret_tests
    base_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(base_dir, "..", "secret_tests", "driver.py")
    
    if os.path.exists(driver_path):
        os.system(f"{sys.executable} {driver_path}")
    else:
        print("Evaluation Driver not found.")

if __name__ == "__main__":
    run_tests()
