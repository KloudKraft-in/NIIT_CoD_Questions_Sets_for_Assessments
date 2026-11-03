#student_workspace/run.py

import importlib.util
import os
import sys

# Add path to secret_tests
secret_tests_path = os.path.join(os.path.dirname(__file__), "..", "secret_tests")
sys.path.insert(0, secret_tests_path)

# Import and run driver
driver_module = importlib.util.spec_from_file_location("driver", os.path.join(secret_tests_path, "driver.py"))
driver = importlib.util.module_from_spec(driver_module)
driver_module.loader.exec_module(driver)

# Run tests
solution_file = os.path.join(os.path.dirname(__file__), "solution.py")
driver.test_student_code(solution_file)