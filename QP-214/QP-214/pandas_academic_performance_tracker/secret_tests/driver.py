import importlib.util
import os
import sys
import pandas as pd
import random

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable."
    return True, None

# Embedded Reference Logic for Grading (QP-221 Style)
class _GradingLogic:
    @staticmethod
    def get_subject_averages(df_g):
        avg = df_g.groupby('Subject')['Marks'].mean()
        return {k: round(float(v), 2) for k, v in avg.to_dict().items()}

    @staticmethod
    def calculate_cgpa(df_m):
        df = df_m.copy()
        df['Weight'] = (df['Marks'] / 10) * df['Credits']
        grp = df.groupby('Student_ID').agg({'Weight': 'sum', 'Credits': 'sum'})
        grp['CGPA'] = grp['Weight'] / grp['Credits']
        return {k: round(float(v), 2) for k, v in grp['CGPA'].to_dict().items()}

    @staticmethod
    def identify_anomalies(df_m):
        diff = df_m.groupby('Student_ID')['Marks'].agg(lambda x: x.max() - x.min())
        anoms = diff[diff > 20].index.tolist()
        names = df_m[df_m['Student_ID'].isin(anoms)]['Name'].unique().tolist()
        return sorted(names)

def test_student_code(solution_path):
    report_dir = os.path.dirname(solution_path)
    report_path = os.path.join(report_dir, "report.txt")
    
    # Load Student Solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        msg = f"IMPORT ERROR: {e}"
        print(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write(msg + "\n")
        return

    print("Running Tests for: Academic Performance Tracker (Professional Edition)\n")
    report_lines = ["Running Tests for: Academic Performance Tracker (Professional Edition)\n"]

    if not hasattr(solution, "PerformanceManager"):
        msg = "ERROR: PerformanceManager class not found in solution.py"
        print(msg); report_lines.append(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")
        return

    # Data Paths
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    info_p = os.path.join(data_dir, "student_info.csv")
    grades_p = os.path.join(data_dir, "academic_grades.csv")
    
    try:
        raw_info = pd.read_csv(info_p)
        raw_grades = pd.read_csv(grades_p)
        merged_ref = pd.merge(raw_info, raw_grades, on="Student_ID")
    except Exception as e:
        print(f"CRITICAL ERROR: Data missing. {e}"); return

    def compare_rounded(r, e, precision=1):
        try:
            if isinstance(r, (float, int)): return round(float(r), precision) == round(float(e), precision)
            if isinstance(r, dict):
                return all(compare_rounded(r[k], e.get(k)) for k in e)
            if isinstance(r, list):
                return sorted(str(x) for x in r) == sorted(str(y) for y in e)
            return str(r) == str(e)
        except: return False

    test_cases = [
        {
            "desc": "Initialize and Load internal DataFrames",
            "func": "load_records",
            "setup": lambda: solution.PerformanceManager(),
            "call": lambda obj: (obj.load_records(info_p, grades_p), isinstance(obj.df_info, pd.DataFrame)),
            "check": lambda res: res[1] == True,
            "expected_output": "PerformanceManager.df_info should be a DataFrame after loading.",
            "marks": 0
        },
        {
            "desc": "Verify Inner Join merging logic",
            "func": "get_merged_data",
            "setup": lambda: _inject_data(solution.PerformanceManager(), raw_info, raw_grades),
            "call": lambda obj: obj.get_merged_data(),
            "check": lambda res: len(res) == len(merged_ref) and 'Marks' in res.columns,
            "expected_output": "Merged DataFrame count should match inner join count.",
            "marks": 3
        },
        {
            "desc": "Aggregate mean marks per subject",
            "func": "get_subject_averages",
            "setup": lambda: solution.AcademicAnalyst(),
            "call": lambda obj: obj.get_subject_averages(raw_grades),
            "check": lambda res: compare_rounded(res, _GradingLogic.get_subject_averages(raw_grades)),
            "expected_output": "Dict of mean marks for each subject.",
            "marks": 3
        },
        {
            "desc": "Weighted multi-column math (CGPA)",
            "func": "calculate_cgpa",
            "setup": lambda: solution.AcademicAnalyst(),
            "call": lambda obj: obj.calculate_cgpa(merged_ref),
            "check": lambda res: compare_rounded(res, _GradingLogic.calculate_cgpa(merged_ref)) if isinstance(res, (pd.Series, dict)) else False,
            "expected_output": "Accurate CGPA calculation (sum(marks*credits)/sum(credits)).",
            "marks": 3
        },
        {
            "desc": "Complex deviation logic (Anomaly detection)",
            "func": "identify_anomalies",
            "setup": lambda: solution.AcademicAnalyst(),
            "call": lambda obj: obj.identify_anomalies(merged_ref),
            "check": lambda res: compare_rounded(res, _GradingLogic.identify_anomalies(merged_ref)),
            "expected_output": "List of student names where Max - Min marks > 20.",
            "marks": 3
        },
        {
            "desc": "Filter records by numeric threshold",
            "func": "find_top_students",
            "setup": lambda: solution.AcademicAnalyst(),
            "call": lambda obj: obj.find_top_students(merged_ref, 8.5),
            "check": lambda res: isinstance(res, list) and len(res) > 0,
            "expected_output": "List of names with CGPA above threshold.",
            "marks": 4
        },
        {
            "desc": "Row identification for Max value",
            "func": "subject_topper",
            "setup": lambda: solution.AcademicAnalyst(),
            "call": lambda obj: obj.subject_topper(merged_ref, "Math"),
            "check": lambda res: "Alex Brown" in str(res) and "95" in str(res),
            "expected_output": "Correct topper name and marks for Math.",
            "marks": 4
        }
    ]

    total_score = 0
    for idx, case in enumerate(test_cases, 1):
        marks = case["marks"]
        try:
            obj = case["setup"]()
            valid, err = validate_method_exists(obj, case["func"])
            if not valid:
                msg = f"FAIL TC{idx} [{case['desc']}]: {err}"
                print(msg); report_lines.append(msg); continue

            result = case["call"](obj)
            passed = case["check"](result)

            if passed:
                total_score += marks
                msg = f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})"
            else:
                msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks})\n  Expected: {case['expected_output']}\n  Got: {repr(result)}"
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}] (0/{marks}) | Error: {type(e).__name__}: {e}"
        print(msg); report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/20.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

def _inject_data(obj, i, g):
    obj.df_info = i.copy()
    obj.df_grades = g.copy()
    return obj

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
