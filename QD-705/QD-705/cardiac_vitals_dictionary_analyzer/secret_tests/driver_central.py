import importlib.util
import os
import sys
from io import StringIO
from datetime import datetime
import pytz

def test_student_code(solution_path, vm_tag=None):
    """Central server test runner with IST timestamp support."""
    
    # Setup paths
    if vm_tag:
        report_dir = f"/home/ubuntu/central_server/reports/cardiac_vitals_dictionary_analyzer/{vm_tag}"
        os.makedirs(report_dir, exist_ok=True)
        ist = pytz.timezone('Asia/Kolkata')
        raw_timestamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
        timestamp = raw_timestamp.replace(':', '-') if sys.platform == 'win32' else raw_timestamp
        report_path = os.path.join(report_dir, f"{vm_tag}_{timestamp}.txt")
    else:
        report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
        report_path = os.path.join(report_dir, "report.txt")
        os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    print("Running Tests for: Cardiac Vitals Dictionary Analyzer\n")
    report_lines = ["Running Tests for: Cardiac Vitals Dictionary Analyzer\n"]

    test_cases = [
        {
            "desc": "Initial State",
            "func": "__init__",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: print(str(obj.records)),
            "check": lambda output: "'PatientID': 'P01'" in output and "'HeartRate': 72" in output and "'HeartRate': None" in output,
            "marks": 0
        },
        {
            "desc": "Clean Records",
            "func": "clean_records",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.clean_records(),
            "check": lambda output: "Removed Records: 2" in output,
            "marks": 4
        },
        {
            "desc": "Find Highest Rate",
            "func": "find_highest_rate",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.find_highest_rate(),
            "check": lambda output: "Highest Heart Rate: 110" in output,
            "marks": 4
        },
        {
            "desc": "Patient Averages",
            "func": "patient_averages",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.patient_averages(),
            "check": lambda output: "P01: 72.33" in output and "P02: 85.00" in output and "P03: 107.50" in output and "P04: 71.50" in output and "P05: 85.00" in output,
            "marks": 4
        },
        {
            "desc": "High Risk Identification",
            "func": "high_risk",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.high_risk(100),
            "check": lambda output: "High Risk Patients: P03" in output,
            "marks": 4
        },
        {
            "desc": "Count High Risk Patients",
            "func": "count_high_risk",
            "setup": lambda: student_module.HealthMonitor(),
            "call": lambda obj: obj.count_high_risk(100),
            "check": lambda output: "High Risk Patient Count: 1" in output,
            "marks": 4
        }
    ]

    visible_score = 0
    visible_max = 0
    hidden_score = 0
    hidden_max = 0
    total_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 4)
        is_hidden = case.get("is_hidden", False)
        
        if not is_hidden:
            visible_max += marks
        else:
            hidden_max += marks
        
        try:
            obj = case["setup"]()
            
            # Capture stdout for methods that print
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                case["call"](obj)
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            # Execute test check
            passed = case["check"](output)
            
            if passed:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"PASS {test_type} Test Case {idx} Passed: {case['desc']}"
                if not is_hidden:
                    visible_score += marks
                else:
                    hidden_score += marks
                total_score += marks
            else:
                test_type = "Hidden" if is_hidden else "Visible"
                msg = f"FAIL {test_type} Test Case {idx} Failed: {case['desc']} | Reason: Output mismatch"
            
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            test_type = "Hidden" if is_hidden else "Visible"
            msg = f"FAIL {test_type} Test Case {idx} Crashed: {case['desc']} | Error: {str(e)}"
            print(msg)
            report_lines.append(msg)

    # Format score line based on vm_tag (central vs local)
    if vm_tag:
        score_line = f"\nSCORE: {visible_score}/{visible_max} (Visible) + {hidden_score}/{hidden_max} (Hidden) = {total_score}/20.0 (Total)"
    else:
        score_line = f"\nSCORE: {visible_score}/{visible_max} (Visible)"
    
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    vm_tag = sys.argv[1] if len(sys.argv) > 1 else None
    test_student_code(solution_file, vm_tag)
