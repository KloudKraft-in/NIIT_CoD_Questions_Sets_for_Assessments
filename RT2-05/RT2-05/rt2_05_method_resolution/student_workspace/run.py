import os
import sys

# Standardized Evaluation Harness for RT2-05: Custom Method Resolution
# This script triggers the driver.py located in the secret_tests folder.

def main():
    # Set the path to the driver
    driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "secret_tests", "driver.py"))
    
    if not os.path.exists(driver_path):
        print(f"❌ Error: Evaluation driver not found at {driver_path}")
        sys.exit(1)

    # Import the driver and run evaluation
    sys.path.append(os.path.dirname(driver_path))
    try:
        import driver
        driver.test_student_code()
    except Exception as e:
        print(f"❌ Error executing driver: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
