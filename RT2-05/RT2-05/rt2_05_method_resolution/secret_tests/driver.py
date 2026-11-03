import subprocess
import os
import sys

def run_test(input_file, solution_path):
    """Runs the solution script with input from a file and returns the output."""
    try:
        with open(input_file, 'r') as f:
            input_str = f.read()

        process = subprocess.Popen(
            [sys.executable, solution_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=input_str)
        if stderr:
            return stderr.strip(), False
        return stdout.strip(), True
    except Exception as e:
        return str(e), False

def test_student_code(solution_path=None):
    if solution_path is None:
        solution_path = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    
    test_cases_dir = os.path.join(os.path.dirname(__file__), "test_cases")
    if not os.path.exists(test_cases_dir):
        print(f"ERROR: Test cases directory not found at {test_cases_dir}")
        return

    print("Running Local Evaluation for: Custom Method Resolution (HR-Style)\n")
    print(f"{'Test Case':<15} | {'Status':<10} | {'Marks'}")
    print("-" * 40)

    total_score = 0
    test_files = sorted([f for f in os.listdir(test_cases_dir) if f.startswith("input")])[:15]
    
    # Standardized TC Names for RT2-05 Custom Method Resolution
    TC_NAMES = [
        "Sample Case 0 - 1 then 2",
        "Sample Case 1 - 2 twice",
        "Multiple Fun1 Calls",
        "Multiple Fun2 Calls",
        "Interleaved 1 and 2",
        "Alternating Calls",
        "All Fun1 Sequence",
        "All Fun2 Sequence",
        "Single Call Case (1)",
        "Single Call Case (2)",
        "Volume Test - 5 Calls",
        "Volume Test - 10 Calls",
        "Random Sequence 1",
        "Random Sequence 2",
        "Max Load Sequence Test"
    ]
    
    for i, in_file in enumerate(test_files):
        in_path = os.path.join(test_cases_dir, in_file)
        out_path = os.path.join(test_cases_dir, in_file.replace("input", "output"))
        
        if not os.path.exists(out_path):
            continue

        with open(out_path, 'r') as f:
            expected = f.read().strip()

        actual, success = run_test(in_path, solution_path)
        
        # Normalize for comparison
        expected_norm = "\n".join([line.strip() for line in expected.splitlines() if line.strip()])
        actual_norm = "\n".join([line.strip() for line in actual.splitlines() if line.strip()])

        marks_per_case = 30 // len(test_files)
        tc_desc = TC_NAMES[i] if i < len(TC_NAMES) else f"Test {i+1}"

        if not success:
            status = "ERROR"
            print(f"\n[RUNTIME ERROR in TC{i+1}]:\n{actual}\n")
        elif actual_norm == expected_norm:
            status = "PASSED"
            total_score += marks_per_case
        else:
            status = "FAILED"
            print(f"\n[OUTPUT MISMATCH in TC{i+1}]:")
            print(f"Expected (first 50 chars): {expected_norm[:50]}...")
            print(f"Actual   (first 50 chars): {actual_norm[:50]}...\n")

        print(f"TC{i+1:02d} [{tc_desc[:30]:<30}] | {status:<10} | {marks_per_case if status == 'PASSED' else 0}/{marks_per_case}")

    print("-" * 40)
    total_possible_marks = len(test_files) * marks_per_case
    print(f"{'TOTAL SCORE':<15} | {'':<10} | {total_score}/{total_possible_marks}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_student_code(sys.argv[1])
    else:
        test_student_code()
