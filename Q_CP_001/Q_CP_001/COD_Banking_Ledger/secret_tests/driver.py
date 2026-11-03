import os
import shutil
import subprocess

def test_student_code(solution_path):
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(os.path.dirname(solution_path), "report.txt")
    
    # Target directory for the build
    build_dest = os.path.join(base_dir, "src", "Solution.cpp")
    os.makedirs(os.path.dirname(build_dest), exist_ok=True)
    
    # 2. Preparation: Copy student code
    shutil.copy(solution_path, build_dest)
    
    print("Running Tests for: Banking Ledger System (C++ LLD)\n")
    report_lines = ["Running Tests for: Banking Ledger System (C++ LLD)\n"]
    
    # 3. Execution: Compile and Run
    try:
        print("Compiling C++ code...")
        test_file = os.path.join(base_dir, "tests", "test_runner.cpp")
        binary_out = os.path.join(base_dir, "run_tests")
        
        if os.name == 'nt':
            binary_out += ".exe"
            
        compile_res = subprocess.run(
            ["g++", "-std=c++17", test_file, "-o", binary_out],
            capture_output=True, text=True
        )
        
        if compile_res.returncode != 0:
            print("--- COMPILATION FAILED ---")
            print(compile_res.stderr)
            report_lines.append("COMPILATION FAILED")
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("\n".join(report_lines) + "\n")
            return
        
        print("Running compiled tests...")
        run_res = subprocess.run([binary_out], capture_output=True, text=True)
        results_text = run_res.stdout + run_res.stderr
        
        # 4. Parsing Output
        total_score = 0.0
        
        test_mapping = {
            "testOpenAccount": ("TC2 [Account Registration Logic]", 1.0),
            "testDeposit": ("TC3 [Deposit Logic]", 2.0),
            "testWithdraw": ("TC4 [Withdrawal with Constraints]", 3.0),
            "testGetTransactionHistory": ("TC5 [Audit Trail Retrieval]", 1.0),
            "testTotalBankLiquidity": ("TC6 [Network Liquidity Summation]", 1.0),
            "testApplyInterest": ("TC7 [Bulk Interest Sweep]", 2.0)
        }
        
        for method, (tc_name, marks) in test_mapping.items():
            if f"[  PASSED  ] TestSuite.{method}" in results_text:
                msg = f"PASS {tc_name} ({marks}/{marks})"
                total_score += marks
            else:
                msg = f"FAIL {tc_name} (0/{marks})"
            
            print(msg)
            report_lines.append(msg)
        
        score_line = f"\nTOTAL SCORE: {total_score}/10.0"
        print(score_line)
        report_lines.append(score_line)
        
        # 5. Output report
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
            
    except Exception as e:
        print(f"Error during evaluation: {e}")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "student_workspace", "solution.cpp")
    test_student_code(sol_file)
