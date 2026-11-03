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

    print("Running Tests for: Event Manager\n")
    report_lines = ["Running Tests for: Event Manager\n"]

    # Verify class exists
    if not hasattr(student_module, "EventManager"):
        error_msg = "ERROR: EventManager class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    test_cases = [
        {
            "desc": "Initialize empty event registry",
            "func": "initialize",
            "setup": lambda: student_module.EventManager(),
            "call": lambda obj: (isinstance(obj.events, dict), len(obj.events)),
            "check": lambda result: result[0] and result[1] == 0,
            "expected_output": "Empty dictionary initialized",
            "marks": 5
        },
        {
            "desc": "Successfully add a new event",
            "func": "add_event",
            "setup": lambda: student_module.EventManager(),
            "call": lambda obj: (obj.add_event("event1", {"name": "Login", "type": "auth"}), obj.add_event("event2", {"name": "Error", "type": "error"})),
            "check": lambda result: result[0] is True and result[1] is True,
            "expected_output": "Both events added successfully (both return True)",
            "marks": 5
        },
        {
            "desc": "Retrieve the dictionary of all events",
            "func": "fetch_all",
            "setup": lambda: _setup_fetch_all(student_module),
            "call": lambda obj: obj.fetch_all(),
            "check": lambda result: isinstance(result, dict) and len(result) == 3 and "event1" in result,
            "expected_output": "Dictionary with all 3 events returned",
            "marks": 5
        },
        {
            "desc": "Correctly update an existing event",
            "func": "update_event",
            "setup": lambda: _setup_update_event(student_module),
            "call": lambda obj: (obj.update_event("event1", {"name": "Updated Login", "type": "auth"}), obj.events["event1"]),
            "check": lambda result: result[0] is True and result[1].get("name") == "Updated Login",
            "expected_output": "Event updated successfully with new data",
            "marks": 5
        },
        {
            "desc": "Correctly delete an event resource",
            "func": "delete_event",
            "setup": lambda: _setup_delete_event(student_module),
            "call": lambda obj: (obj.delete_event("event1"), len(obj.events)),
            "check": lambda result: result[0] is True and result[1] == 2,
            "expected_output": "Event deleted successfully, events count reduced from 3 to 2",
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
                method_exists, error_msg = validate_method_exists(student_module.EventManager(), case["func"])
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
        
        except KeyError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Key Not Found\n"
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
        score_line += "\n⚠️ No tests passed. Make sure to implement all required methods."
    
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_fetch_all(student_module):
    """Setup for fetch_all test."""
    manager = student_module.EventManager()
    manager.events = {
        "event1": {"name": "Login", "type": "auth"},
        "event2": {"name": "Error", "type": "error"},
        "event3": {"name": "Logout", "type": "auth"}
    }
    return manager


def _setup_update_event(student_module):
    """Setup for update_event test."""
    manager = student_module.EventManager()
    manager.events = {
        "event1": {"name": "Login", "type": "auth"},
        "event2": {"name": "Error", "type": "error"}
    }
    return manager


def _setup_delete_event(student_module):
    """Setup for delete_event test."""
    manager = student_module.EventManager()
    manager.events = {
        "event1": {"name": "Login", "type": "auth"},
        "event2": {"name": "Error", "type": "error"},
        "event3": {"name": "Logout", "type": "auth"}
    }
    return manager


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
