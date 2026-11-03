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
        { "name": "Mixed Electronics/Furniture", "input": "4\nLaptop Electronics 1200.0 5\nMouse Electronics 25.0 10\nChair Furniture 150.0 0\nDesk Furniture 300.0 2", "expected": "Total Inventory Value: 6850.00\nMost Expensive (Electronics): Laptop\nMost Expensive (Furniture): Desk" },
        { "name": "Zero Stock Filtering", "input": "2\nApple Fruit 1.5 0\nBanana Fruit 0.5 100", "expected": "Total Inventory Value: 50.00\nMost Expensive (Fruit): Banana" },
        { "name": "Stationery Batch", "input": "3\nPen Stationery 10.0 100\nPencil Stationery 5.0 200\nNotebook Stationery 50.0 10", "expected": "Total Inventory Value: 2500.00\nMost Expensive (Stationery): Notebook" },
        { "name": "High Value IT", "input": "2\nServer IT 5000.0 1\nWorkstation IT 3000.0 2", "expected": "Total Inventory Value: 11000.00\nMost Expensive (IT): Server" },
        { "name": "Mixed Small Batch", "input": "3\nBread Food 2.0 50\nMilk Food 1.5 20\nSoap Home 5.0 10", "expected": "Total Inventory Value: 180.00\nMost Expensive (Food): Bread\nMost Expensive (Home): Soap" },
        { "name": "Minimal Stock", "input": "2\nItem1 Test 10.0 0\nItem2 Test 20.0 1", "expected": "Total Inventory Value: 20.00\nMost Expensive (Test): Item2" },
        { "name": "Identical Prices", "input": "2\nAlpha Tech 100.0 5\nBeta Tech 100.0 10", "expected": "Total Inventory Value: 1500.00\nMost Expensive (Tech): Alpha" },
        { "name": "Float Precision", "input": "1\nPartX Mech 12.34 10", "expected": "Total Inventory Value: 123.40\nMost Expensive (Mech): PartX" },
        { "name": "Multi-Category Variety", "input": "3\nA Cat1 10 1\nB Cat2 20 1\nC Cat3 30 1", "expected": "Total Inventory Value: 60.00\nMost Expensive (Cat1): A\nMost Expensive (Cat2): B\nMost Expensive (Cat3): C" },
        { "name": "Single Item Stream", "input": "1\nItemX Misc 50.0 2", "expected": "Total Inventory Value: 100.00\nMost Expensive (Misc): ItemX" }
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
