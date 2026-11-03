import subprocess
import os
import sys

def run_test(input_str):
    try:
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        process = subprocess.Popen(
            ['java', 'Harness'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=parent_dir
        )
        stdout, stderr = process.communicate(input=input_str)
        if stderr: return stderr.strip(), False
        return stdout.strip(), True
    except Exception as e: return str(e), False

def compile_java():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    solution_path = "student_workspace/Solution.java"
    harness_path = "secret_tests/Harness.java"
    base_path = "student_workspace/Base.java"
    files = [solution_path, harness_path, base_path]
    result = subprocess.run(['javac', '-d', '.'] + files, capture_output=True, text=True, cwd=parent_dir)
    return result.returncode == 0, result.stderr

def execute():
    success, err = compile_java()
    if not success:
        print(f"Compilation Failed:\n{err}")
        sys.exit(1)

    test_cases = [
        { "name": "Savings Min Balance Failure", "input": "2\nSavings ACC01 1000 Deposit 100\nSavings ACC01 1100 Withdraw 700", "expected": "Deposit Successful: New Balance: 1100.0\nWithdrawal Failed: Minimum balance requirement not met." },
        { "name": "Savings Valid Withdrawal", "input": "1\nSavings ACC01 1000 Withdraw 400", "expected": "Withdrawal Successful: New Balance: 600.0" },
        { "name": "Savings Deposit", "input": "1\nSavings ACC03 500 Deposit 500", "expected": "Deposit Successful: New Balance: 1000.0" },
        { "name": "Current Overdraft Success", "input": "1\nCurrent ACC02 100 Withdraw 1500", "expected": "Withdrawal Successful: New Balance: -1400.0" },
        { "name": "Current Overdraft Failure", "input": "2\nCurrent ACC02 100 Deposit 100\nCurrent ACC02 200 Withdraw 3000", "expected": "Deposit Successful: New Balance: 200.0\nWithdrawal Failed: Minimum balance requirement not met." },
        { "name": "Current Deposit", "input": "1\nCurrent ACC05 200 Deposit 800", "expected": "Deposit Successful: New Balance: 1000.0" },
        { "name": "Mixed Batch Success", "input": "2\nSavings ACC10 2000 Withdraw 1000\nCurrent ACC11 0 Withdraw 500", "expected": "Withdrawal Successful: New Balance: 1000.0\nWithdrawal Successful: New Balance: -500.0" },
        { "name": "Mixed Batch Failure", "input": "2\nSavings ACC20 500 Deposit 100\nCurrent ACC21 -1500 Withdraw 600", "expected": "Deposit Successful: New Balance: 600.0\nWithdrawal Failed: Minimum balance requirement not met." },
        { "name": "Zero Amount Transaction", "input": "2\nSavings ACC30 1000 Deposit 0\nCurrent ACC31 500 Withdraw 0", "expected": "Deposit Successful: New Balance: 1000.0\nWithdrawal Successful: New Balance: 500.0" },
        { "name": "Large Value Transaction", "input": "1\nCurrent ACC99 10000 Deposit 90000", "expected": "Deposit Successful: New Balance: 100000.0" }
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
