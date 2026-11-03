"""
Test Launcher for QP-211: Store Sales Monitor
Executes all visible test cases and generates report.
"""

import importlib.util
import os

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "solution.py")
    
    # Load the driver module
    driver_path = os.path.join(os.path.dirname(__file__), "..", "secret_tests", "driver.py")
    spec = importlib.util.spec_from_file_location("driver", driver_path)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    
    # Run tests
    driver.test_student_code(solution_file)
