import importlib.util
import os
import sys
from io import StringIO

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(student_module)
    except Exception as e:
        print(f"IMPORT ERROR: {e}")
        return

    print("Running Tests for: Student Exam Advanced Operations Dictionary (Independent Mode)\n")
    report_lines = ["Running Tests for: Student Exam Advanced Operations Dictionary (Independent Mode)\n"]

    if not hasattr(student_module, "StudentResultManager"):
        print("ERROR: StudentResultManager class not found")
        return

    StudentResultManager = student_module.StudentResultManager
    
    # Shared test data derived from the problem sample
    test_data = {
        "S001": {"name": "Arjun", "math": 85, "science": 92, "english": 78},
        "S002": {"name": "Nisha", "math": 95, "science": 88, "english": 90},
        "S003": {"name": "Rohan", "math": 72, "science": 79, "english": 85},
        "S004": {"name": "Divya", "math": 88, "science": 95, "english": 92},
        "S005": {"name": "Karan", "math": 80, "science": 82, "english": 88}
    }

    test_cases = [
        {
            "desc": "Calculate student averages",
            "func": "calculate_student_averages",
            "expected": ["'S001': 85.0", "'S004': 91.7"],
            "marks": 7
        },
        {
            "desc": "Find highest average student",
            "func": "find_highest_average",
            "expected": ["Highest Average: Divya (S004) - 91.7"],
            "marks": 7
        },
        {
            "desc": "Calculate subject-wise averages",
            "func": "calculate_subject_averages",
            "expected": ["'math': 84.0", "'science': 87.2", "'english': 86.6"],
            "marks": 6
        }
    ]

    total_score = 0
    max_score = 20.0

    for idx, case in enumerate(test_cases, 1):
        try:
            obj = StudentResultManager()
            # Injection point for independence
            obj.students = test_data.copy()
            
            if not hasattr(obj, case["func"]):
                msg = f"FAIL TC{idx} [{case['desc']}] | Method '{case['func']}' missing"
                print(msg); report_lines.append(msg); continue

            # Capture stdout
            old_stdout = sys.stdout
            new_stdout = StringIO()
            sys.stdout = new_stdout
            try:
                getattr(obj, case["func"])()
                output = new_stdout.getvalue().strip()
            finally:
                sys.stdout = old_stdout

            # Check for all expected snippets
            passed = all(snippet in output for snippet in case["expected"])
            
            if passed:
                msg = f"PASS TC{idx} [{case['desc']}] ({case['marks']}/{case['marks']})"
                total_score += case["marks"]
            else:
                msg = f"FAIL TC{idx} [{case['desc']}] | Expected snippets: {case['expected']}, Got: {repr(output)}"
            
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}] | Error: {str(e)}"
        
        print(msg)
        report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/{max_score}"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
