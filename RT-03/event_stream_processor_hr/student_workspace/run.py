import os
import sys

# Add the secret_tests directory to the path so we can import the driver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'secret_tests')))

from driver import test_student_code

if __name__ == "__main__":
    solution_path = os.path.join(os.path.dirname(__file__), "solution.py")
    test_student_code(solution_path)
