import importlib.util
import os
import sys
import random
from io import StringIO

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try: spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    print("Running Tests for: Student Exam Dictionary (QD-720) (15 Marks Mode)\n")
    report_lines = ["Running Tests for: Student Exam Dictionary (QD-720) (15 Marks Mode)\n"]

    if not hasattr(solution, "StudentResultManager"):
        print("ERROR: StudentResultManager class not found"); return
    
    StudentResultManager = solution.StudentResultManager
    base_data = {
        "S001": {"name": "Arjun", "math": 85, "science": 92, "english": 78},
        "S002": {"name": "Nisha", "math": 95, "science": 88, "english": 90},
        "S003": {"name": "Rohan", "math": 72, "science": 79, "english": 85},
        "S004": {"name": "Divya", "math": 88, "science": 95, "english": 92},
        "S005": {"name": "Karan", "math": 80, "science": 82, "english": 88}
    }

    # PDF Alignment for QD-720: TC1(5), TC2(5), TC3(5) = 15 Total
    tc_configs = [
        ("Calculate average score for each student", 5),
        ("Find student with highest average score", 5),
        ("Calculate subject-wise averages", 5)
    ]

    random.seed(None)
    rv = random.randint(80, 100)

    total_score = 0
    max_score = 15.0

    for i, (desc, marks) in enumerate(tc_configs, 1):
        try:
            def run_t(idx, data):
                obj = StudentResultManager()
                obj.students = {k: v.copy() for k, v in data.items()}
                old_stdout, new_stdout = sys.stdout, StringIO()
                sys.stdout = new_stdout
                try:
                    if idx == 1: obj.calculate_student_averages()
                    elif idx == 2: obj.find_highest_average()
                    elif idx == 3: obj.calculate_subject_averages()
                    return new_stdout.getvalue().strip()
                finally: sys.stdout = old_stdout

            # DUAL RUN
            out1 = run_t(i, base_data)
            
            mod_data = {k: v.copy() for k, v in base_data.items()}
            if i == 1: mod_data["S001"].update({"math":rv,"science":rv,"english":rv})
            elif i == 2: mod_data["S005"].update({"math":100,"science":100,"english":100})
            elif i == 3: [v.update({"math":0}) for v in mod_data.values()]
            
            out2 = run_t(i, mod_data)
            
            if i == 1: exp2 = f"'S001': {float(rv)}"
            elif i == 2: exp2 = "Karan (S005) - 100.0"
            elif i == 3: exp2 = "'math': 0.0"

            passed, hardcoded = False, False
            if out1 == out2 and exp2 not in out2: hardcoded = True
            elif exp2 in out2: passed = True

            if passed:
                total_score += marks
                msg = f"PASS TC{i} [{desc}] ({marks}/{marks})"
            elif hardcoded:
                msg = f"FAIL TC{i} [{desc}] (0/{marks}) - Hardcoded"
            else:
                msg = f"FAIL TC{i} [{desc}] (0/{marks})"

        except Exception as e: msg = f"FAIL TC{i} | Error: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/{max_score}"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
