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

def validate_return_type(result, expected_type, method_name):
    """Validate return type with helpful error message."""
    if result is None:
        return False, f"Method '{method_name}' returned None. Make sure to return the required value, not just pass."
    if expected_type == str and not isinstance(result, str):
        return False, f"Method '{method_name}' should return a string, but returned {type(result).__name__}: {repr(result)}"
    if expected_type == int and not isinstance(result, int):
        return False, f"Method '{method_name}' should return an integer, but returned {type(result).__name__}: {repr(result)}"
    if expected_type == dict and not isinstance(result, dict):
        return False, f"Method '{method_name}' should return a dictionary, but returned {type(result).__name__}: {repr(result)}"
    if expected_type == list and not isinstance(result, list):
        return False, f"Method '{method_name}' should return a list, but returned {type(result).__name__}: {repr(result)}"
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
        error_msg = f"SYNTAX ERROR: {str(e)}\nFix the syntax error in solution.py before running tests."
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return

    print("Running Tests for: Online Course Manager\n")
    report_lines = ["Running Tests for: Online Course Manager\n"]

    # Verify class exists
    if not hasattr(student_module, "CourseManager"):
        error_msg = "ERROR: CourseManager class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    test_cases = [
        {
            "desc": "Initialize manager structure",
            "func": "initialize",
            "setup": lambda: student_module.CourseManager(),
            "call": lambda obj: obj.courses,
            "check": lambda result: isinstance(result, dict) and len(result) == 0,
            "expected_output": "courses attribute as empty dictionary {}",
            "expected_type": dict,
            "marks": 5
        },
        {
            "desc": "Add course to manager",
            "func": "add_course",
            "setup": lambda: student_module.CourseManager(),
            "call": lambda obj: (obj.add_course("PY101", "Python Basics", 2), obj.courses.get("PY101")),
            "check": lambda result: isinstance(result, tuple) and result[1] == {"title": "Python Basics", "max": 2, "students": []},
            "expected_output": "course structure with keys: 'title', 'max', 'students' (as empty list)",
            "expected_type": dict,
            "marks": 5
        },
        {
            "desc": "Register student to course",
            "func": "register_student",
            "setup": lambda: _setup_register(student_module),
            "call": lambda obj: (obj.register_student("PY101", "Bob"), obj.courses["PY101"]["students"]),
            "check": lambda result: isinstance(result, tuple) and "Enrolled in Python Basics" in result[0] and "Bob" in result[1],
            "expected_output": "enrollment message containing 'Enrolled in [course_title]' and student added to course's students list",
            "expected_type": str,
            "marks": 5
        },
        {
            "desc": "Get available seats in course",
            "func": "get_available_seats",
            "setup": lambda: _setup_seats(student_module),
            "call": lambda obj: obj.get_available_seats("PY101"),
            "check": lambda result: result == 1,
            "expected_output": "available seats count (capacity - enrolled students). Expected: 1 (2 capacity - 1 enrolled)",
            "expected_type": int,
            "marks": 5
        },
        {
            "desc": "Remove student from course",
            "func": "remove_student",
            "setup": lambda: _setup_remove(student_module),
            "call": lambda obj: (obj.remove_student("PY101", "Bob"), "Bob" in obj.courses["PY101"]["students"]),
            "check": lambda result: isinstance(result, tuple) and "Removed Bob from Python Basics" in result[0] and result[1] == False,
            "expected_output": "removal message containing 'Removed [name] from [course_title]' and student removed from students list",
            "expected_type": str,
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
                method_exists, error_msg = validate_method_exists(student_module.CourseManager(), case["func"])
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
            msg += f"  Hint: Check method signature and ensure you're passing required parameters"
            print(msg)
            report_lines.append(msg)
        
        except KeyError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Key Not Found\n"
            msg += f"  Details: Trying to access key {str(e)} that doesn't exist\n"
            msg += f"  Hint: Check if you're storing data with correct keys: 'title', 'max', 'students' in course dict"
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Review the method implementation for logic errors or missing edge case handling"
            print(msg)
            report_lines.append(msg)

    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")




def _setup_register(student_module):
    """Setup for register student test."""
    manager = student_module.CourseManager()
    manager.add_course("PY101", "Python Basics", 2)
    return manager


def _setup_seats(student_module):
    """Setup for available seats test."""
    manager = student_module.CourseManager()
    manager.add_course("PY101", "Python Basics", 2)
    manager.register_student("PY101", "Bob")
    return manager


def _setup_remove(student_module):
    """Setup for remove student test."""
    manager = student_module.CourseManager()
    manager.add_course("PY101", "Python Basics", 2)
    manager.register_student("PY101", "Bob")
    return manager


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
