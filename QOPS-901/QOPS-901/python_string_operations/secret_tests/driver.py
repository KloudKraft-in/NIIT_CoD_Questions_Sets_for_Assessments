import os
import sys
import importlib.util
import io
import contextlib

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found in class. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable. Make sure it's defined as a method."
    return True, None

def test_student_code(solution_path):
    """Main test function that runs all test cases"""
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    # Clear previous report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("")

    # Load the student's solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(solution)
    except SyntaxError as e:
        error_msg = f"SYNTAX ERROR: {str(e)}\nFix the syntax error in solution.py before running tests."
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return
    except Exception as e:
        error_msg = f"IMPORT ERROR: {str(e)}\nMake sure all required modules are imported correctly"
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return
    
    print("Running Tests for: Python String Operations\n")
    report_lines = ["Running Tests for: Python String Operations\n"]
    
    # Verify class exists
    if not hasattr(solution, "Solution"):
        error_msg = "ERROR: Solution class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return
    
    Solution = solution.Solution
    
    test_cases = [
        {
            "desc": "Convert to uppercase",
            "func": "convert_to_uppercase",
            "setup": lambda: _setup_tc1(Solution),
            "call": lambda obj: obj.convert_to_uppercase("python programming language"),
            "check": lambda result, output: "PYTHON PROGRAMMING LANGUAGE" in output,
            "expected_output": "Printed 'PYTHON PROGRAMMING LANGUAGE'",
            "marks": 5
        },
        {
            "desc": "Convert to lowercase",
            "func": "convert_to_lowercase",
            "setup": lambda: _setup_tc2(Solution),
            "call": lambda obj: obj.convert_to_lowercase("WELCOME TO PYTHON"),
            "check": lambda result, output: "welcome to python" in output,
            "expected_output": "Printed 'welcome to python'",
            "marks": 5
        },
        {
            "desc": "Capitalize first letter",
            "func": "capitalize_sentence",
            "setup": lambda: _setup_tc3(Solution),
            "call": lambda obj: obj.capitalize_sentence("python is easy to learn"),
            "check": lambda result, output: "Python is easy to learn" in output,
            "expected_output": "Printed 'Python is easy to learn'",
            "marks": 5
        },
        {
            "desc": "Count word occurrences",
            "func": "count_word_occurrences",
            "setup": lambda: _setup_tc4(Solution),
            "call": lambda obj: obj.count_word_occurrences("...", "data"),
            "check": lambda result, output: "2" in output,
            "expected_output": "Printed '2'",
            "marks": 5
        },
        {
            "desc": "Replace word",
            "func": "replace_word",
            "setup": lambda: _setup_tc5(Solution),
            "call": lambda obj: obj.replace_word("...", "Python", "Java"),
            "check": lambda result, output: "Java is a powerful language" in output,
            "expected_output": "Printed 'Java is a powerful language'",
            "marks": 5
        },
        {
            "desc": "Split sentence",
            "func": "split_sentence",
            "setup": lambda: _setup_tc6(Solution),
            "call": lambda obj: obj.split_sentence("..."),
            "check": lambda result, output: "['Python', 'makes', 'data', 'analysis', 'easier']" in output or "'Python', 'makes', 'data', 'analysis', 'easier'" in output,
            "expected_output": "Printed list of words",
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 5)
        max_score += marks
        
        try:
            # Verify method exists
            method_exists, error_msg = validate_method_exists(Solution(), case["func"])
            if not method_exists:
                msg = f"FAIL TC{idx} [{case['desc']}]: {error_msg}"
                print(msg)
                report_lines.append(msg)
                continue
            
            # Setup and execute test with stdout capture
            obj = case["setup"]()
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                result = case["call"](obj)
            output = f.getvalue()
            
            passed = case["check"](result, output)
            
            if passed:
                msg = f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})"
                total_score += marks
            else:
                msg = f"FAIL TC{idx} [{case['desc']}]\n"
                msg += f"  Expected: {case['expected_output']}\n"
                msg += f"  Captured Output: {repr(output.strip())}\n"
            
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}\n"
            print(msg)
            report_lines.append(msg)

    # ============ FINAL SCORING ============
    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_tc1(Solution):
    return Solution()

def _setup_tc2(Solution):
    return Solution()

def _setup_tc3(Solution):
    return Solution()

def _setup_tc4(Solution):
    return Solution()

def _setup_tc5(Solution):
    return Solution()

def _setup_tc6(Solution):
    return Solution()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solution_path = sys.argv[1]
    else:
        solution_path = os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.py')
    test_student_code(solution_path)
