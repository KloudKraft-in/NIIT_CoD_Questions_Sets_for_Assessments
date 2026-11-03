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
    slug = "Cpp_Track_Banking_Ledger"

    match = re.search(r'(.+)_(\d{8}_\d{6})', vm_tag)
    if match:
        username, timestamp = match.groups()
    else:
        username, timestamp = vm_tag, get_ist_time()

    report_base = f"/home/ubuntu/central_server/reports/{slug}/{username}"
    if os.name == 'nt':
        report_base = os.path.join(os.path.dirname(solution_path), "reports", username)
        
    os.makedirs(report_base, exist_ok=True)
    report_path = os.path.join(report_base, f"{username}_{timestamp}.txt")

    results = [f"Running Tests for: {slug} (Central Server - C++ Mode)\n"]
    total_score = 0
    base_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        abs_solution_path = os.path.abspath(solution_path)
        if not os.path.exists(abs_solution_path):
            raise FileNotFoundError(f"Solution file not found at {abs_solution_path}")

        build_dest = os.path.join(base_dir, "src", "Solution.cpp")
        os.makedirs(os.path.dirname(build_dest), exist_ok=True)
        shutil.copy(abs_solution_path, build_dest)

        test_file = os.path.join(base_dir, "tests", "test_runner.cpp")
        binary_out = os.path.join(base_dir, "run_tests")
        if os.name == 'nt':
            binary_out += ".exe"

        compile_res = subprocess.run(
            ["g++", "-std=c++17", test_file, "-o", binary_out],
            capture_output=True, text=True
        )

        if compile_res.returncode != 0:
            results.append("COMPILATION FAILED")
            results.append(compile_res.stderr)
        else:
            run_res = subprocess.run([binary_out], capture_output=True, text=True)
            results_text = run_res.stdout + run_res.stderr

            tc_configs = [
                {"desc": "TC1: Instantiate complex structures", "method": "testOpenAccount", "m": 0},
                {"desc": "TC2: Add account with initial log", "method": "testOpenAccount", "m": 1},
                {"desc": "TC3: Deposit with log tracking", "method": "testDeposit", "m": 2},
                {"desc": "TC4: Withdraw with overdraft logic", "method": "testWithdraw", "m": 3},
                {"desc": "TC5: Retrieve full transaction trail", "method": "testGetTransactionHistory", "m": 1},
                {"desc": "TC6: Calculate total bank liquidity", "method": "testTotalBankLiquidity", "m": 1},
                {"desc": "TC7: Perform bulk interest sweep", "method": "testApplyInterest", "m": 2}
            ]

            for idx, case in enumerate(tc_configs, 1):
                marks = float(case["m"])
                method = case["method"]
                desc = case["desc"]
                
                if f"[  PASSED  ] TestSuite.{method}" in results_text:
                    total_score += marks
                    results.append(f"PASS TC{idx} [{desc}] ({marks}/{marks})")
                else:
                    results.append(f"FAIL TC{idx} [{desc}] (0/{marks}) - Incorrect logic or execution error.")

    except Exception as e:
        results.append(f"CRITICAL SYSTEM ERROR: {traceback.format_exc()}")

    results.append(f"\nSCORE: {total_score}/10 (Visible) | {total_score}/10 (Total)")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results) + "\n")
    
    print(f"✅ Report generated at: {report_path}")

if __name__ == "__main__":
    v_tag = sys.argv[1] if len(sys.argv) > 1 else "DEFAULT"
    s_path = sys.argv[2] if len(sys.argv) > 2 else "/home/ubuntu/submissions/solution.cpp"
    test_student_code(s_path, v_tag)
