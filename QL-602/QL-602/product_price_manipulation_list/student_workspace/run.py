import sys
import os

# Add parent directory to path to import driver
current_dir = os.path.dirname(os.path.abspath(__file__))
secret_tests_dir = os.path.join(current_dir, "..", "secret_tests")
sys.path.insert(0, secret_tests_dir)

from driver import test_student_code

if __name__ == "__main__":
    solution_file = os.path.join(current_dir, "solution.py")
    test_student_code(solution_file)
