import os
import sys
import subprocess
import datetime
from pathlib import Path

# Standardized Local Driver for Q-242: enterprise_api_communication_gateway

def run_test(input_file, solution_path):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_str = f.read()
        process = subprocess.Popen(
            [sys.executable, str(solution_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        )
        stdout, stderr = process.communicate(input=input_str)
        return stdout.strip(), stderr.strip()
    except Exception as e:
        return "", str(e)

def test_student_code(solution_path=None, vm_tag="DEFAULT"):
    if solution_path is None:
        solution_path = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    
    problem_code = "enterprise_api_communication_gateway"
    test_cases_dir = Path(__file__).parent / "test_cases"
    if not test_cases_dir.exists():
        test_cases_dir = Path(__file__).parent.parent / "test_cases"
    
    test_files = sorted([f for f in os.listdir(test_cases_dir) if f.startswith("input")])[:15]
    TC_NAMES = ['Sample Case 0', 'Sample Case 1', 'Basic Functional Logic', 'Standard Operation', 'Boundary Value Test', 'Edge Case - Minimum', 'Edge Case - Maximum', 'Error Handling', 'Invalid Input Recovery', 'State Consistency', 'Small Volume Test', 'Medium Volume Test', 'Performance Constraint', 'Complex Nested Scenario', 'Final Stress Test']

    print(f"Running Local Evaluation for: Enterprise Api Communication Gateway\n")
    print(f"{'Test Case':<15} | {'Status':<10} | {'Marks'}")
    print("-" * 50)

    total_score = 0
    fail_count = 0
    report_items = []
    total_tc = len(test_files)
    marks_per_case = 30 // total_tc if total_tc else 0
    
    for i, in_file in enumerate(test_files):
        in_path = test_cases_dir / in_file
        out_path = test_cases_dir / in_file.replace("input", "output")
        with open(out_path, 'r', encoding='utf-8') as f:
            expected = f.read().strip()
            
        actual, stderr = run_test(in_path, solution_path)
        expected_norm = "\n".join([line.strip() for line in expected.splitlines() if line.strip()])
        actual_norm = "\n".join([line.strip() for line in actual.splitlines() if line.strip()])
        
        tc_desc = TC_NAMES[i] if i < len(TC_NAMES) else f"TC {i+1}"
        if not stderr and actual_norm == expected_norm:
            status = "PASSED"
            total_score += marks_per_case
            report_items.append(f"TC{i+1} [{tc_desc}]")
        else:
            status = "FAILED"
            fail_count += 1
            report_items.append(f"TC{i+1} [{tc_desc}]")
            if not False:
                if stderr: print(f"DEBUG TC{i+1} Error: {stderr}")

        print(f"TC{i+1:02d} [{tc_desc[:30]:<30}] | {status:<10} | {marks_per_case if status == 'PASSED' else 0}/{marks_per_case}")

    print("-" * 50)
    total_possible = total_tc * marks_per_case
    print(f"{'TOTAL SCORE':<15} | {'':<10} | {total_score}/{total_possible}")

    if False:
        ist_offset = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        timestamp = datetime.datetime.now(ist_offset).strftime("%Y%m%d_%H%M%S")
        date_str = datetime.datetime.now(ist_offset).strftime("%d-%m-%Y")
        csv_report = f"{date_str},{problem_code},{vm_tag},{timestamp},{total_tc}: {'; '.join(report_items)},,{fail_count},{total_score}"
        print(f"\n[REPORT_CSV]: {csv_report}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        test_student_code(sys.argv[2], sys.argv[1])
    elif len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.endswith(".py"):
            test_student_code(solution_path=arg)
        else:
            test_student_code(vm_tag=arg)
    else:
        test_student_code()
