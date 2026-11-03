import os
import sys
import subprocess
import re
from datetime import datetime, timezone, timedelta

def get_ist_time():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y%m%d_%H%M%S")

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

def run_test(input_str, harness_class_name):
    try:
        java_bin = get_java_cmd('java')
        env = os.environ.copy()
        if java_bin != 'java':
            bin_dir = os.path.dirname(java_bin)
            env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")

        process = subprocess.Popen(
            [java_bin, '-cp', '.', harness_class_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=".",
            env=env
        )
        stdout, stderr = process.communicate(input=input_str)
        if stderr: return stderr.strip(), False
        return stdout.strip(), True
    except Exception as e: return str(e), False

def compile_java(harness_dir, solution_path):
    harness_files = [f for f in os.listdir(harness_dir) if f.endswith(".java") and f != os.path.basename(solution_path)]
    if not harness_files:
        return False, f"Harness file not found in {harness_dir}"
    
    harness_path = os.path.join(harness_dir, harness_files[0])
    all_files = [solution_path, harness_path]
    javac_bin = get_java_cmd('javac')
    
    env = os.environ.copy()
    if javac_bin != 'javac':
        bin_dir = os.path.dirname(javac_bin)
        env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")

    result = subprocess.run([javac_bin, '-d', '.'] + all_files, capture_output=True, text=True, cwd=".", env=env)
    harness_class = os.path.splitext(harness_files[0])[0]
    return result.returncode == 0, (harness_class if result.returncode == 0 else result.stderr)

def test_student_code(solution_path, vm_tag="DEFAULT"):
    match = re.search(r'(.+)_(\d{8}_\d{6})', vm_tag)
    if match: username, timestamp = match.groups()
    else: username, timestamp = vm_tag, get_ist_time()

    slug = "java_smart_home_energy_monitor"
    report_base = f"/home/ubuntu/central_server/reports/{slug}/{username}"
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{username}_{timestamp}.txt")

    harness_dir = os.path.dirname(os.path.abspath(__file__))
    
    success, output = compile_java(harness_dir, solution_path)
    if not success:
        with open(report_path, "w") as f: 
            f.write(f"COMPILATION ERROR:\n{output}")
        print(f"❌ Compilation failed: {output}")
        return

    # To run successfully on systems where the class inside Harness.java is HarnessJ07:
    harness_class_name = output
    if harness_class_name == "Harness":
        harness_class_name = "HarnessJ07"

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

    results = [f"Running Tests for: {slug} (Central Server) - Log Optimized\n"]
    total_score = 0
    total_possible = len(test_cases) * 3
    
    for i, tc in enumerate(test_cases, 1):
        actual, success = run_test(tc["input"] + "\n", harness_class_name)
        
        expected_norm = " ".join(tc["expected"].lower().split())
        actual_norm = " ".join(actual.lower().split())
        
        marks = 3
        is_passed = success and expected_norm in actual_norm
        
        if is_passed:
            total_score += marks
            results.append(f"PASS TC{i} [{tc['name']}] ({marks}/{marks})")
        else:
            results.append(f"FAIL TC{i} [{tc['name']}] (0/{marks})")

    results.append(f"\nSCORE: {total_score}/{total_possible} (Visible) | {total_score}/{total_possible} (Total)")
    
    with open(report_path, "w") as f:
        f.write("\n".join(results) + "\n")
    
    current_date = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d-%m-%Y")
    csv_row = f"{current_date},{slug},{username},{timestamp},Total Score: {total_score}/{total_possible},,{total_score}"
    print(csv_row)

if __name__ == "__main__":
    vm = sys.argv[1] if len(sys.argv) > 1 else "DEFAULT"
    sol = sys.argv[2] if len(sys.argv) > 2 else "Solution.java"
    test_student_code(os.path.abspath(sol), vm)
