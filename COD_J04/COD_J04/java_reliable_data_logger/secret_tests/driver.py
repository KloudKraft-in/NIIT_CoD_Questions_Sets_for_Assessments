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
        { "name": "Standard Log Validation", "input": "3\n[10:00:00] INFO System Started\n10:05:00 WARN Disk space low\n[10:10:00] FATAL Memory overflow", "expected": "Log Processed: INFO\nError: Log must start with a bracketed timestamp.\nError: Invalid log level: FATAL." },
        { "name": "Full Valid Stream", "input": "2\n[08:00:00] ERROR Database Down\n[09:30:00] WARN Network Lag", "expected": "Log Processed: ERROR\nLog Processed: WARN" },
        { "name": "Unsupported Level FATAL", "input": "1\n[12:00:00] FATAL Kernel Panic", "expected": "Error: Invalid log level: FATAL." },
        { "name": "Unsupported Level TRACE", "input": "1\n[12:01:00] TRACE Function Enter", "expected": "Error: Invalid log level: TRACE." },
        { "name": "Missing Timestamp Brackets", "input": "1\n08:00:00 INFO No Brackets", "expected": "Error: Log must start with a bracketed timestamp." },
        { "name": "Empty Log Line", "input": "1\n ", "expected": "Error: Log must start with a bracketed timestamp." },
        { "name": "Partial Valid Stream", "input": "3\n[11:00:00] INFO Heartbeat\n[11:05:00] DEBUG Verbose Log\n[11:10:00] WARN High Latency", "expected": "Log Processed: INFO\nError: Invalid log level: DEBUG.\nLog Processed: WARN" },
        { "name": "Timestamp and Level Only", "input": "1\n[00:00:00] INFO", "expected": "Log Processed: INFO" },
        { "name": "Leading Spaces", "input": "1\n [01:00:00] INFO Space", "expected": "Error: Log must start with a bracketed timestamp." },
        { "name": "Malformed Separator", "input": "1\n[10:00:00]-INFO-Dash", "expected": "Error: Invalid log level: [10:00:00]-INFO-Dash." }
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
