import os
import sys
import subprocess
from pathlib import Path

# Local Driver for QP-227
def run_test(input_file, solution_path):
    try:
        with open(input_file, 'r') as f:
            input_str = f.read()
        process = subprocess.Popen(
            [sys.executable, str(solution_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=input_str)
        return stdout.strip(), stderr.strip()
    except Exception as e:
        return "", str(e)

def test_student_code(solution_path=None):
    if solution_path is None:
        solution_path = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    
    test_cases_dir = os.path.join(os.path.dirname(__file__), "test_cases")
    test_files = sorted([f for f in os.listdir(test_cases_dir) if f.startswith("input")])
    
    print(f"{'Test Case':<25} | {'Status':<10} | {'Marks'}")
    print("-" * 50)

    total_score = 0
    marks_per_case = 30 // len(test_files)
    
    for i, in_file in enumerate(test_files):
        in_path = os.path.join(test_cases_dir, in_file)
        out_path = os.path.join(test_cases_dir, in_file.replace("input", "output"))
        
        with open(out_path, 'r') as f:
            expected = f.read().strip()

        actual, stderr = run_test(in_path, solution_path)
        
        expected_norm = "\n".join([line.strip() for line in expected.splitlines() if line.strip()])
        actual_norm = "\n".join([line.strip() for line in actual.splitlines() if line.strip()])

        if not stderr and actual_norm == expected_norm:
            status = "PASSED"
            total_score += marks_per_case
        else:
            status = "FAILED"
            print(f"DEBUG: TC{i+1} FAILED")
            print(f"DEBUG: Expected: {repr(expected_norm)}")
            print(f"DEBUG: Actual:   {repr(actual_norm)}")

        print(f"TC{i+1:02d} | {status:<10} | {marks_per_case if status == 'PASSED' else 0}/{marks_per_case}")

    print("-" * 50)
    print(f"TOTAL SCORE: {total_score}/30")

if __name__ == "__main__":
    test_student_code()
