import importlib.util
import os

# Get paths
script_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(script_dir, "..", "secret_tests", "driver.py")
solution_path = os.path.join(script_dir, "solution.py")

# Load and run driver tests
spec = importlib.util.spec_from_file_location("driver", driver_path)
driver_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver_module)

driver_module.test_student_code(solution_path)
