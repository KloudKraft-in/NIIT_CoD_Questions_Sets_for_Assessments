import subprocess
import os
import sys

def get_java_cmd(cmd_name):
    try:
        res = subprocess.run([cmd_name, '-version'], capture_output=True, text=True)
        output = (res.stdout or "") + (res.stderr or "")
        if res.returncode == 0 and len(output.strip()) > 0:
            return cmd_name
    except Exception:
        pass

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
            [java_bin, 'HarnessJ07'],
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
            "name": "Sample Case 0 - Standard Overload", 
            "input": "3\nConstant Fridge 150.0\nVariable AC 2000.0 0.6\nVariable TV 100.0 0.3\n24 2200.0", 
            "expected": "Total Consumption: 33120.00 Wh\nPeak Device: AC\nError: Overload detected: Current load is 2250.0W, which exceeds limit of 2200.0W." 
        },
        { 
            "name": "No Overload Success", 
            "input": "3\nConstant Fridge 150.0\nVariable AC 2000.0 0.6\nVariable TV 100.0 0.3\n24 2500.0", 
            "expected": "Total Consumption: 33120.00 Wh\nPeak Device: AC" 
        },
        { 
            "name": "Constant Only Load", 
            "input": "2\nConstant Bulb 60.0\nConstant Router 15.0\n10 100.0", 
            "expected": "Total Consumption: 750.00 Wh\nPeak Device: Bulb" 
        },
        { 
            "name": "Variable Only Load", 
            "input": "2\nVariable Heater 1500.0 0.5\nVariable Fan 80.0 0.8\n5 2000.0", 
            "expected": "Total Consumption: 4070.00 Wh\nPeak Device: Heater" 
        },
        { 
            "name": "Zero Hours Monitoring", 
            "input": "2\nConstant Fridge 150.0\nVariable AC 2000.0 0.6\n0 2500.0", 
            "expected": "Total Consumption: 0.00 Wh\nPeak Device: Fridge" 
        },
        { 
            "name": "Single Device Overload", 
            "input": "1\nConstant Microwave 1200.0\n1 1000.0", 
            "expected": "Total Consumption: 1200.00 Wh\nPeak Device: Microwave\nError: Overload detected: Current load is 1200.0W, which exceeds limit of 1000.0W." 
        },
        { 
            "name": "Empty Device List", 
            "input": "0\n24 2000.0", 
            "expected": "Total Consumption: 0.00 Wh\nPeak Device: None" 
        },
        { 
            "name": "Tie in Peak Device", 
            "input": "2\nConstant Bulb1 60.0\nConstant Bulb2 60.0\n10 200.0", 
            "expected": "Total Consumption: 1200.00 Wh\nPeak Device: Bulb1" 
        },
        { 
            "name": "High Load No Overload Boundary", 
            "input": "2\nConstant DeviceA 1000.0\nVariable DeviceB 500.0 0.5\n10 1500.0", 
            "expected": "Total Consumption: 12500.00 Wh\nPeak Device: DeviceA" 
        },
        { 
            "name": "Overload Boundary Failure", 
            "input": "2\nConstant DeviceA 1000.0\nVariable DeviceB 500.0 0.5\n10 1499.9", 
            "expected": "Total Consumption: 12500.00 Wh\nPeak Device: DeviceA\nError: Overload detected: Current load is 1500.0W, which exceeds limit of 1499.9W." 
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
