import importlib.util
import os
import sys

# Set up paths
current_dir = os.path.dirname(os.path.abspath(__file__))
solution_path = os.path.join(current_dir, "solution.py")
driver_path = os.path.abspath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))

def main():
    if not os.path.exists(driver_path):
        print(f"Error: Driver not found at {driver_path}")
        return

    # Load driver module
    spec = importlib.util.spec_from_file_location("driver", driver_path)
    driver_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(driver_module)
        # Call the test function
        driver_module.test_student_code(solution_path)
    except Exception as e:
        print(f"Error executing driver: {e}")

if __name__ == "__main__":
    main()
