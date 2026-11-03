import importlib.util
import os
import sys
import pandas as pd

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found in class. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable. Make sure it's defined as a method."
    return True, None

def detect_hardcoding(obj, test_scenarios):
    """
    Detect hardcoding by running same method with different inputs.
    Returns (is_hardcoded, details)
    """
    results = {}
    
    for scenario_name, method_calls in test_scenarios.items():
        try:
            scenario_results = []
            for call_func in method_calls:
                result = call_func(obj)
                scenario_results.append(repr(result))
            results[scenario_name] = scenario_results
        except Exception as e:
            results[scenario_name] = [f"ERROR: {str(e)}"]
    
    # Check if hardcoding: same result for different inputs in same method
    for scenario_name, result_list in results.items():
        # If all results are identical for different inputs, likely hardcoded
        if len(set(result_list)) == 1 and len(result_list) > 1:
            return True, f"Hardcoding detected in {scenario_name}: all inputs return same result"
    
    return False, None

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    # Clear previous report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("")

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(student_module)
    except SyntaxError as e:
        error_msg = f"SYNTAX ERROR: {str(e)}\nFix the syntax error in solution.py before running tests."
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return
    except ImportError as e:
        error_msg = f"IMPORT ERROR: {str(e)}\nMake sure pandas is imported correctly"
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return

    print("Running Tests for: Student Performance Tracker\n")
    report_lines = ["Running Tests for: Student Performance Tracker\n"]

    # Verify class exists
    if not hasattr(student_module, "StudentTracker"):
        error_msg = "ERROR: StudentTracker class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    test_cases = [
        {
            "desc": "Initialize empty DataFrame structure",
            "func": "initialize",
            "setup": lambda: student_module.StudentTracker(),
            "call": lambda obj: (isinstance(obj.data, pd.DataFrame), list(obj.data.columns)),
            "check": lambda result: result[0] and result[1] == ['StudentName', 'Score', 'Subject'],
            "expected_output": "DataFrame with columns ['StudentName', 'Score', 'Subject'] (empty initially)",
            "marks": 5
        },
        {
            "desc": "Add records to DataFrame",
            "func": "record_grade",
            "setup": lambda: _setup_record(student_module),
            "call": lambda obj: (len(obj.data), obj.data['StudentName'].tolist()),
            "check": lambda result: result[0] == 3 and 'Alice' in result[1] and 'Bob' in result[1],
            "expected_output": "3 records added with correct student names",
            "marks": 5
        },
        {
            "desc": "Calculate average score for subject",
            "func": "get_subject_avg",
            "setup": lambda: _setup_subject_avg(student_module),
            "call": lambda obj: obj.get_subject_avg("Math"),
            "check": lambda result: abs(result - 85.0) < 0.01,
            "expected_output": "Average score for Math = 85.0 (Alice 85 + Bob 85) / 2",
            "marks": 5
        },
        {
            "desc": "Get top scorers by threshold",
            "func": "get_top_scorers",
            "setup": lambda: _setup_top_scorers(student_module),
            "call": lambda obj: sorted(obj.get_top_scorers(80)),
            "check": lambda result: result == ['Alice', 'Bob'],
            "expected_output": "List of unique student names with scores > 80: ['Alice', 'Bob']",
            "marks": 5
        },
        {
            "desc": "Get summary statistics",
            "func": "get_summary_stats",
            "setup": lambda: _setup_summary(student_module),
            "call": lambda obj: obj.get_summary_stats(),
            "check": lambda result: result.get('total_records') == 4 and result.get('unique_students') == 3,
            "expected_output": "Dictionary with total_records=4, unique_students=3",
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0
    malpractice_detected = False

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 5)
        max_score += marks
        
        try:
            # Verify method exists (skip for initialization test)
            if case["func"] != "initialize":
                method_exists, error_msg = validate_method_exists(student_module.StudentTracker(), case["func"])
                if not method_exists:
                    msg = f"FAIL TC{idx} [{case['desc']}]: {error_msg}"
                    print(msg)
                    report_lines.append(msg)
                    continue
            
            # Setup and execute test
            obj = case["setup"]()
            result = case["call"](obj)
            passed = case["check"](result)
            
            if passed:
                msg = f"PASS TC{idx} [{case['desc']}]"
                total_score += marks
            else:
                # Provide detailed mismatch error
                msg = f"FAIL TC{idx} [{case['desc']}]\n"
                msg += f"  Expected: {case['expected_output']}\n"
                msg += f"  Got: {repr(result)}\n"
                msg += f"  Hint: Check your logic in '{case['func']}' method"
            
            print(msg)
            report_lines.append(msg)
        
        except TypeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Argument Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check method signature and parameter types"
            print(msg)
            report_lines.append(msg)
        
        except KeyError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Key Not Found\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check column names in DataFrame: 'StudentName', 'Score', 'Subject'"
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Review DataFrame operations and pandas methods used"
            print(msg)
            report_lines.append(msg)

    # ============ HARDCODING DETECTION ============
    print("\n--- Hardcoding Detection ---")
    
    hardcode_test_scenarios = {
        "get_subject_avg with different subjects": [
            lambda obj: obj.get_subject_avg("Math"),
            lambda obj: obj.get_subject_avg("Science"),
            lambda obj: obj.get_subject_avg("English")
        ],
        "get_top_scorers with different thresholds": [
            lambda obj: obj.get_top_scorers(70),
            lambda obj: obj.get_top_scorers(80),
            lambda obj: obj.get_top_scorers(90)
        ]
    }
    
    # Setup data for hardcoding test
    try:
        hardcode_obj = student_module.StudentTracker()
        hardcode_obj.record_grade("Alice", 85, "Math")
        hardcode_obj.record_grade("Bob", 90, "Math")
        hardcode_obj.record_grade("Charlie", 75, "Science")
        hardcode_obj.record_grade("Diana", 88, "Science")
        
        is_hardcoded, hardcode_detail = detect_hardcoding(hardcode_obj, hardcode_test_scenarios)
        
        if is_hardcoded:
            malpractice_detected = True
            msg = f"⚠️ POTENTIAL HARDCODING DETECTED\n  {hardcode_detail}"
            print(msg)
            report_lines.append(msg)
        else:
            print("✓ No hardcoding detected - methods respond to input variations")
    except Exception as e:
        print(f"  Hardcoding check skipped (error: {str(e)})")

    # ============ FINAL SCORING ============
    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    if malpractice_detected:
        score_line += "\n⚠️ WARNING: Potential hardcoding detected. Submission flagged for review."
    
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_record(student_module):
    """Setup for record_grade test."""
    tracker = student_module.StudentTracker()
    tracker.record_grade("Alice", 85, "Math")
    tracker.record_grade("Bob", 90, "Science")
    tracker.record_grade("Charlie", 78, "English")
    return tracker


def _setup_subject_avg(student_module):
    """Setup for get_subject_avg test."""
    tracker = student_module.StudentTracker()
    tracker.record_grade("Alice", 85, "Math")
    tracker.record_grade("Bob", 85, "Math")
    tracker.record_grade("Charlie", 92, "Science")
    return tracker


def _setup_top_scorers(student_module):
    """Setup for get_top_scorers test."""
    tracker = student_module.StudentTracker()
    tracker.record_grade("Alice", 88, "Math")
    tracker.record_grade("Bob", 82, "Science")
    tracker.record_grade("Charlie", 70, "English")
    return tracker


def _setup_summary(student_module):
    """Setup for get_summary_stats test."""
    tracker = student_module.StudentTracker()
    tracker.record_grade("Alice", 85, "Math")
    tracker.record_grade("Alice", 90, "Science")
    tracker.record_grade("Bob", 78, "Math")
    tracker.record_grade("Charlie", 88, "English")
    return tracker


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
