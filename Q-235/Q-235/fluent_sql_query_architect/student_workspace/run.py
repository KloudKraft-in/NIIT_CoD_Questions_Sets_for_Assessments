import os
import sys

# Standardized Evaluation Harness for Batch-2
# This script triggers the driver.py located in the secret_tests folder.

def main():
    # Set the path to the driver
    driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "secret_tests", "driver.py"))
    
    if not os.path.exists(driver_path):
        print(f"Error: Evaluation driver not found at {driver_path}")
        sys.exit(1)

    # Add driver directory to sys.path
    sys.path.append(os.path.dirname(driver_path))
    
    try:
        import driver
        # Pass sys.argv[1] to the driver if any
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if arg.endswith(".py"):
                driver.test_student_code(solution_path=arg)
            else:
                driver.test_student_code(vm_tag=arg)
        else:
            driver.test_student_code()
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
