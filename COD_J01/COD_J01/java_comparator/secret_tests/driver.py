import subprocess
import os
import sys

def run_test(input_str):
    try:
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        process = subprocess.Popen(
            ['java', 'HarnessJ01'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=parent_dir
        )
        stdout, stderr = process.communicate(input=input_str)
        if stderr:
            return stderr.strip(), False
        return stdout.strip(), True
    except Exception as e:
        return str(e), False

def compile_java():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    solution_path = "student_workspace/Solution.java"
    harness_path = "secret_tests/Harness.java"
    files = [solution_path, harness_path]
    result = subprocess.run(['javac', '-d', '.'] + files, capture_output=True, text=True, cwd=parent_dir)
    return result.returncode == 0, result.stderr

def execute():
    success, err = compile_java()
    if not success:
        print(f"Compilation Failed:\n{err}")
        sys.exit(1)

    test_cases = [
        { "name": "Mixed Same Batch", "input": "3\n1\nhello\nhello\n2\n10 10\n3\n2 2\n1 2\n1 2", "expected": "Same\nSame\nSame" },
        { "name": "String Mismatch", "input": "1\n1\nhello\nworld", "expected": "Different" },
        { "name": "Case Sensitivity", "input": "1\n1\nJava\njava", "expected": "Different" },
        { "name": "Integer Equality", "input": "1\n2\n500 500", "expected": "Same" },
        { "name": "Integer Mismatch", "input": "1\n2\n10 20", "expected": "Different" },
        { "name": "Array Length Mismatch", "input": "1\n3\n2 3\n1 2\n1 2 3", "expected": "Different" },
        { "name": "Array Content Match", "input": "1\n3\n3 3\n10 20 30\n10 20 30", "expected": "Same" },
        { "name": "Array Content Mismatch", "input": "1\n3\n2 2\n1 2\n1 3", "expected": "Different" },
        { "name": "Empty String Match", "input": "1\n1\n\n", "expected": "Same" },
        { "name": "Single Element Array", "input": "1\n3\n1 1\n100\n100", "expected": "Same" }
    ]

    total_marks = 0
    print("\n" + "="*60)
    print(" JAVA ASSESSMENT EXECUTION ".center(60, "="))
    print("="*60 + "\n")

    for tc in test_cases:
        actual, success = run_test(tc["input"] + "\n")
        expected_norm = "\n".join([l.strip().lower() for l in tc["expected"].splitlines()])
        actual_norm = "\n".join([l.strip().lower() for l in actual.splitlines()])
        
        is_passed = success and actual_norm == expected_norm
        marks = 3 if is_passed else 0
        total_marks += marks
        status = "PASSED" if is_passed else "FAILED"

        print(f"Test Case: {tc['name']}")
        print("-" * 30)
        print(f"Input:\n{tc['input']}")
        print(f"\nExpected Output:\n{tc['expected']}")
        print(f"\nYour Output:\n{actual}")
        print(f"\nStatus: {status} | Marks: {marks}/3")
        print("\n" + "="*60 + "\n")

    print(f"TOTAL SCORE: {total_marks}/{len(test_cases)*3}")
    print("="*60 + "\n")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    execute()
