# run.py
import importlib.util
import os

def run_tests():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.abspath(os.path.join(current_dir, '..', 'secret_tests', 'driver.py'))

    spec = importlib.util.spec_from_file_location("driver", driver_path)
    driver_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver_module)

    driver_module.test_student_code()

if __name__ == "__main__":
    run_tests()
