# 📁 student_workspace/run.py

import importlib.util
import os

def run_tests():
    # Prepare paths
    current_dir = os.path.dirname(__file__)
    solution_path = os.path.join(current_dir, "solution.py")
    driver_path = os.path.abspath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))

    # Check if driver exists
    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"Driver file not found at: {driver_path}")

    # Load and execute driver module
    spec = importlib.util.spec_from_file_location("driver_module", driver_path)
    driver_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver_module)

    # Run tests with solution path
    driver_module.test_student_code(solution_path)

if __name__ == "__main__":
    run_tests()
