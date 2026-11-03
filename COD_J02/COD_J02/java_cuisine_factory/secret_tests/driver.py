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
        { "name": "Mixed Valid/Invalid", "input": "3\nItalian Lasagne\nJapanese Kamameshi\nPolish Marjoram", "expected": "Serving Lasagne(Italian)\nServing Kamameshi(Japanese)\nUnservable cuisine Polish for dish Marjoram" },
        { "name": "Mixed Unservable", "input": "3\nGreek Tzatziki\nMexican Machaca\nChinese Lanian", "expected": "Unservable cuisine Greek for dish Tzatziki\nServing Machaca(Mexican)\nServing Lanian(Chinese)" },
        { "name": "Pure Italian Batch", "input": "2\nItalian Risotto\nItalian Pasta", "expected": "Serving Risotto(Italian)\nServing Pasta(Italian)" },
        { "name": "Pure Japanese Batch", "input": "2\nJapanese Sashimi\nJapanese Umeboshi", "expected": "Serving Sashimi(Japanese)\nServing Umeboshi(Japanese)" },
        { "name": "Pure Mexican Batch", "input": "2\nMexican Fritada\nMexican Cocido", "expected": "Serving Fritada(Mexican)\nServing Cocido(Mexican)" },
        { "name": "Pure Chinese Batch", "input": "2\nChinese Lanian\nChinese Furikake", "expected": "Serving Lanian(Chinese)\nServing Furikake(Chinese)" },
        { "name": "Mixed Valid Full Set", "input": "4\nItalian Lasagne\nJapanese Nori\nMexican Enchilada\nChinese Zosui", "expected": "Serving Lasagne(Italian)\nServing Nori(Japanese)\nServing Enchilada(Mexican)\nServing Zosui(Chinese)" },
        { "name": "All Unservable", "input": "2\nIndian Biryani\nFrench Baguette", "expected": "Unservable cuisine Indian for dish Biryani\nUnservable cuisine French for dish Baguette" },
        { "name": "Large Variety Case", "input": "5\nMexican Picadillo\nJapanese Tsukemono\nItalian Carbonara\nChinese Dash1\nPolish Rye", "expected": "Serving Picadillo(Mexican)\nServing Tsukemono(Japanese)\nServing Carbonara(Italian)\nServing Dash1(Chinese)\nUnservable cuisine Polish for dish Rye" },
        { "name": "Single Success Case", "input": "1\nMexican Chilaquiles", "expected": "Serving Chilaquiles(Mexican)" }
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
