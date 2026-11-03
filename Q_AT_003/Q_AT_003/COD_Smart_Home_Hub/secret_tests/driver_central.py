import os
import sys

# Fix encoding for Windows consoles printing emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import shutil
import subprocess
import re
import traceback
from datetime import datetime, timezone, timedelta

def get_ist_time():
    try:
        ist = timezone(timedelta(hours=5, minutes=30))
        return datetime.now(ist).strftime("%Y%m%d_%H%M%S")
    except:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

def test_student_code(solution_path, vm_tag="DEFAULT"):
    # 1. Robust Path and Slug Discovery
    slug = "Android_Track_Smart_Home_Hub"

    # 2. Report Path Resolution (Central Server Standard)
    match = re.search(r'(.+)_(\d{8}_\d{6})', vm_tag)
    if match:
        username, timestamp = match.groups()
    else:
        username, timestamp = vm_tag, get_ist_time()

    # Central Server Report Base
    report_base = f"/home/ubuntu/central_server/reports/{slug}/{username}"
    # Fallback for local testing (Windows)
    if os.name == 'nt':
        report_base = os.path.join(os.path.dirname(solution_path), "reports", username)
        
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{username}_{timestamp}.txt")

    results = [f"Running Tests for: {slug} (Central Server - Android/Kotlin Mode)\n"]
    total_score = 0
    base_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        # 3. Validation: Check if student solution exists (.kt)
        abs_solution_path = os.path.abspath(solution_path)
        if not os.path.exists(abs_solution_path):
            raise FileNotFoundError(f"Solution file not found at {abs_solution_path}")

        # 4. Preparation: Copy student code to the Gradle testable location
        build_dest = os.path.join(base_dir, "src", "main", "kotlin", "Solution.kt")
        os.makedirs(os.path.dirname(build_dest), exist_ok=True)
        shutil.copy(abs_solution_path, build_dest)

        # 5. Execution: Run Gradle test
        if os.name == 'nt':
            gradle_cmd = [r"C:\gradle-9.4.1\bin\gradle.bat", "test"]
            use_shell = True
        else:
            gradle_cmd = ["gradle", "test"]
            use_shell = False
            
        result = subprocess.run(gradle_cmd, capture_output=True, text=True, shell=use_shell, cwd=base_dir)
        results_text = result.stdout + result.stderr

        # 6. Test Case Configuration & Scoring (Mapping to the LLD Marks Table)
        tc_configs = [
            {"desc": "TC1: Instantiate complex structures", "method": "testAddDevice", "m": 0},
            {"desc": "TC2: Add device with initial log", "method": "testAddDevice", "m": 1},
            {"desc": "TC3: Toggle state with log tracking", "method": "testToggleDevice", "m": 2},
            {"desc": "TC4: Schedule timer with state constraints", "method": "testScheduleTimer", "m": 3},
            {"desc": "TC5: Retrieve full activity trail of device", "method": "testGetDeviceHistory", "m": 1},
            {"desc": "TC6: Calculate total network power consumption", "method": "testTotalPowerConsumption", "m": 1},
            {"desc": "TC7: Perform bulk turn off sweep", "method": "testTurnOffAllDevices", "m": 2}
        ]

        # 7. Parsing JUnit output for "PASSED" markers
        for idx, case in enumerate(tc_configs, 1):
            marks = float(case["m"])
            method = case["method"]
            desc = case["desc"]
            
            if f" > {method}() PASSED" in results_text:
                total_score += marks
                results.append(f"PASS TC{idx} [{desc}] ({marks}/{marks})")
            else:
                results.append(f"FAIL TC{idx} [{desc}] (0/{marks}) - Incorrect logic or compilation error.")

    except Exception as e:
        results.append(f"CRITICAL SYSTEM ERROR: {traceback.format_exc()}")

    # 8. Final Scoring Report
    results.append(f"\nSCORE: {total_score}/10 (Visible) | {total_score}/10 (Total)")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results) + "\n")
    
    print(f"✅ Report generated at: {report_path}")

if __name__ == "__main__":
    v_tag = sys.argv[1] if len(sys.argv) > 1 else "DEFAULT"
    s_path = sys.argv[2] if len(sys.argv) > 2 else "/home/ubuntu/submissions/solution.kt"
    test_student_code(s_path, v_tag)
