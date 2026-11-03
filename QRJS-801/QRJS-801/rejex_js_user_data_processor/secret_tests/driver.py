import importlib.util
import os
import sys

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found in class. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable. Make sure it's defined as a method."
    return True, None

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
        error_msg = f"SYNTAX ERROR: {str(e)}"
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return

    print("Running Tests for: User Data Processor\n")
    report_lines = ["Running Tests for: User Data Processor\n"]

    # Verify class exists
    if not hasattr(student_module, "UserDataProcessor"):
        error_msg = "ERROR: UserDataProcessor class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    test_cases = [
        {
            "desc": "Validate email addresses",
            "func": "validate_email",
            "setup": lambda: student_module.UserDataProcessor(),
            "call": lambda obj: (obj.validate_email("user@test.com"), obj.validate_email("invalid-email")),
            "check": lambda result: result[0] is True and result[1] is False,
            "expected_output": "Valid email returns True, invalid email returns False",
            "marks": 5
        },
        {
            "desc": "Validate username (5-10 chars alphanumeric)",
            "func": "validate_username",
            "setup": lambda: student_module.UserDataProcessor(),
            "call": lambda obj: (obj.validate_username("admin123"), obj.validate_username("abc")),
            "check": lambda result: result[0] is True and result[1] is False,
            "expected_output": "Valid username returns True, invalid username returns False",
            "marks": 5
        },
        {
            "desc": "Clean phone (extract digits)",
            "func": "clean_phone",
            "setup": lambda: student_module.UserDataProcessor(),
            "call": lambda obj: obj.clean_phone("123-456 7890"),
            "check": lambda result: result == "1234567890",
            "expected_output": "Extracted digits: '1234567890'",
            "marks": 5
        },
        {
            "desc": "Convert dict to JSON (indent=4)",
            "func": "to_json",
            "setup": lambda: student_module.UserDataProcessor(),
            "call": lambda obj: obj.to_json({"id": 1, "name": "test"}),
            "check": lambda result: isinstance(result, str) and "id" in result and "1" in result,
            "expected_output": "JSON formatted string with proper indentation",
            "marks": 5
        },
        {
            "desc": "Parse JSON string to dict",
            "func": "from_json",
            "setup": lambda: student_module.UserDataProcessor(),
            "call": lambda obj: obj.from_json('{"name": "Alice"}'),
            "check": lambda result: result == {"name": "Alice"},
            "expected_output": "Parsed dict: {'name': 'Alice'}",
            "marks": 5
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 5)
        max_score += marks
        
        try:
            # Verify method exists (skip for initialization test)
            if case["func"] != "initialize":
                method_exists, error_msg = validate_method_exists(student_module.UserDataProcessor(), case["func"])
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
                msg = f"FAIL TC{idx} [{case['desc']}]\n"
                msg += f"  Expected: {case['expected_output']}\n"
                msg += f"  Got: {repr(result)}"
            
            print(msg)
            report_lines.append(msg)
        
        except TypeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Type Mismatch Error\n"
            msg += f"  Details: {str(e)}"
            print(msg)
            report_lines.append(msg)
        
        except ValueError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Value Error\n"
            msg += f"  Details: {str(e)}"
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}"
            print(msg)
            report_lines.append(msg)

    # ============ FINAL SCORING ============
    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    
    if total_score == 0:
        score_line += "\nNo tests passed. Make sure to implement all required methods."
    
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_processor(student_module):
    """Setup for validation tests."""
    processor = student_module.UserDataProcessor()
    return processor


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
