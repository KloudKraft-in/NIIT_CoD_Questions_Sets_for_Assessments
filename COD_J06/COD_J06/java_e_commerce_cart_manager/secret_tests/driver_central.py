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

    slug = "java_e_commerce_cart_manager"
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

    # In Repo/J01 structure, harness_class_name is resolved from the filename (e.g. Harness -> which expects Harness.class).
    # Since our Harness file is Harness.java, harness_class_name here resolves to "Harness". 
    # To run successfully on systems where the class inside Harness.java is HarnessJ06:
    # We will run HarnessJ06 if the resolved class name is "Harness" but the class inside Harness.java is HarnessJ06.
    # We can handle this by checking if the harness class name resolved is "Harness", but the compiled class is HarnessJ06.
    # In Repo, on the grading server they might compile and rename the file or run it differently, 
    # but to remain robust locally and globally, let's keep the dynamic harness_class_name detection.
    harness_class_name = output
    if harness_class_name == "Harness":
        harness_class_name = "HarnessJ06"

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
