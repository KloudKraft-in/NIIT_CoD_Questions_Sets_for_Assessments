# run.py
import importlib.util
import os

def run_tests():
    current_dir = os.path.dirname(__file__)
    driver_path = os.path.abspath(os.path.join(current_dir, "..", "secret_tests", "driver.py"))
    solution_path = os.path.abspath(os.path.join(current_dir, "solution.py"))

    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"Driver not found at {driver_path}")
    if not os.path.exists(solution_path):
        raise FileNotFoundError(f"Solution not found at {solution_path}")

    spec = importlib.util.spec_from_file_location("driver", driver_path)
    driver_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver_module)

    driver_module.test_student_code(solution_path)

if __name__ == "__main__":
    run_tests()
