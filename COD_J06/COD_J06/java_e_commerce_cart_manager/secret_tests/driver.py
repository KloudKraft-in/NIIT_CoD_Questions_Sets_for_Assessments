import subprocess
import os
import sys

def get_java_cmd(cmd_name):
    # Check if the command in PATH actually works
    try:
        res = subprocess.run([cmd_name, '-version'], capture_output=True, text=True)
        output = (res.stdout or "") + (res.stderr or "")
        if res.returncode == 0 and len(output.strip()) > 0:
            return cmd_name
    except Exception:
        pass

    # Try standard paths on Windows
    paths = [
        r"C:\Program Files\Java_OLD\jdk-20\bin",
        r"C:\Program Files\Java_OLD\jdk-19\bin",
        r"C:\Program Files\Java\jdk-20\bin",
        r"C:\Program Files\Java\jdk-19\bin",
    ]
    for p in paths:
        full_path = os.path.join(p, cmd_name if os.name != 'nt' else cmd_name + ".exe")
        if os.path.exists(full_path):
            return full_path

    return cmd_name

def run_test(input_str):
    try:
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        java_bin = get_java_cmd('java')
        env = os.environ.copy()
        if java_bin != 'java':
            bin_dir = os.path.dirname(java_bin)
            env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")

        process = subprocess.Popen(
            [java_bin, 'HarnessJ06'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=parent_dir,
            env=env
        )
        stdout, stderr = process.communicate(input=input_str)
        if stderr: return stderr.strip(), False
        return stdout.strip(), True
    except Exception as e: return str(e), False

def compile_java():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    solution_path = "student_workspace/Solution.java"
    harness_path = "secret_tests/Harness.java"
    files = [solution_path, harness_path]
    javac_bin = get_java_cmd('javac')
    
    env = os.environ.copy()
    if javac_bin != 'javac':
        bin_dir = os.path.dirname(javac_bin)
        env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")

    result = subprocess.run([javac_bin, '-d', '.'] + files, capture_output=True, text=True, cwd=parent_dir, env=env)
    return result.returncode == 0, result.stderr

def execute():
    success, err = compile_java()
    if not success:
        print(f"Compilation Failed:\n{err}")
        sys.exit(1)

    test_cases = [
        { 
            "name": "Sample Case 0 - Percentage Discount", 
            "input": "3\nLaptop 1000.00 1 true\nMouse 50.00 2 false\nNotebook 5.00 5 true\nPercentage SAVE10 10.0", 
            "expected": "Subtotal: 1125.00\nDiscount: 112.50\nTax: 102.50\nTotal: 1115.00" 
        },
        { 
            "name": "Flat Discount Success", 
            "input": "2\nShirt 40.00 2 true\nJeans 60.00 1 true\nFlat FLAT15 15.0", 
            "expected": "Subtotal: 140.00\nDiscount: 15.00\nTax: 14.00\nTotal: 139.00" 
        },
        { 
            "name": "Flat Discount Greater than Subtotal", 
            "input": "1\nBook 12.00 1 false\nFlat SUPERDEAL 20.0", 
            "expected": "Subtotal: 12.00\nDiscount: 12.00\nTax: 0.00\nTotal: 0.00" 
        },
        { 
            "name": "No Coupon Applied", 
            "input": "2\nBread 2.50 4 false\nMilk 1.50 2 true\nNone", 
            "expected": "Subtotal: 13.00\nDiscount: 0.00\nTax: 0.30\nTotal: 13.30" 
        },
        { 
            "name": "Empty Coupon Code Exception", 
            "input": "1\nPhone 500.00 1 true\nPercentage   10.0", 
            "expected": "Error: Coupon code cannot be empty." 
        },
        { 
            "name": "Negative Percentage Coupon Exception", 
            "input": "1\nPhone 500.00 1 true\nPercentage INVALID -5.0", 
            "expected": "Error: Invalid discount value." 
        },
        { 
            "name": "Greater Than 100% Coupon Exception", 
            "input": "1\nPhone 500.00 1 true\nPercentage INVALID 105.0", 
            "expected": "Error: Invalid discount value." 
        },
        { 
            "name": "Negative Flat Coupon Exception", 
            "input": "1\nPhone 500.00 1 true\nFlat INVALID -10.0", 
            "expected": "Error: Invalid discount value." 
        },
        { 
            "name": "Empty Cart Total Immediately 0", 
            "input": "0\nPercentage INVALID 150.0", 
            "expected": "Subtotal: 0.00\nDiscount: 0.00\nTax: 0.00\nTotal: 0.00" 
        },
        { 
            "name": "Zero Price Item Valid Checkout", 
            "input": "2\nGiftItem 0.00 1 true\nFreebie 0.00 5 false\nPercentage SAVE20 20.0", 
            "expected": "Subtotal: 0.00\nDiscount: 0.00\nTax: 0.00\nTotal: 0.00" 
        }
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
