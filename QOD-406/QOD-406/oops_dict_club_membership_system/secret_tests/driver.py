import os
import sys
import importlib.util

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
    
    print("Running Tests for: Club Membership System\n")
    report_lines = ["Running Tests for: Club Membership System\n"]
    
    # Verify class exists
    if not hasattr(solution, "MembershipSystem"):
        error_msg = "ERROR: MembershipSystem class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return
    
    MembershipSystem = solution.MembershipSystem
    
    test_cases = [
        {
            "desc": "Check names in blank system",
            "func": "list_all_members",
            "setup": lambda: _setup_tc1(MembershipSystem),
            "call": lambda obj: obj.list_all_members(),
            "check": lambda result: result == [],
            "expected_output": "Empty list []",
            "marks": 1
        },
        {
            "desc": "Register two members",
            "func": "register_member",
            "setup": lambda: _setup_tc2(MembershipSystem),
            "call": lambda obj: len(obj.members),
            "check": lambda result: result == 2,
            "expected_output": "Members dictionary should have 2 entries",
            "marks": 2
        },
        {
            "desc": "Lookup existing member M101",
            "func": "get_member",
            "setup": lambda: _setup_tc3(MembershipSystem),
            "call": lambda obj: obj.get_member("M101"),
            "check": lambda result: result == "Alice",
            "expected_output": "Should return 'Alice'",
            "marks": 2
        },
        {
            "desc": "Lookup missing member M103",
            "func": "get_member",
            "setup": lambda: _setup_tc4(MembershipSystem),
            "call": lambda obj: obj.get_member("M103"),
            "check": lambda result: result == "Not Found",
            "expected_output": "Should return 'Not Found'",
            "marks": 1
        },
        {
            "desc": "Remove member M101 and verify",
            "func": "remove_member",
            "setup": lambda: _setup_tc5(MembershipSystem),
            "call": lambda obj: list(obj.members.keys()),
            "check": lambda result: result == ["M102"],
            "expected_output": "Members dictionary should only contain M102",
            "marks": 2
        },
        {
            "desc": "List only names after removal",
            "func": "list_all_members",
            "setup": lambda: _setup_tc6(MembershipSystem),
            "call": lambda obj: obj.list_all_members(),
            "check": lambda result: result == ["Bob"],
            "expected_output": "Should return ['Bob']",
            "marks": 2
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 1)
        max_score += marks
        
        try:
            # Verify method exists
            method_exists, error_msg = validate_method_exists(MembershipSystem(), case["func"])
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
                msg = f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})"
                total_score += marks
            else:
                # Provide detailed mismatch error
                msg = f"FAIL TC{idx} [{case['desc']}]\n"
                msg += f"  Expected: {case['expected_output']}\n"
                msg += f"  Got: {repr(result)}\n"
                msg += f"  Hint: Review the method implementation and return types"
            
            print(msg)
            report_lines.append(msg)
        
        except AttributeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Attribute Not Found\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check if all required attributes (self.members) are initialized"
            print(msg)
            report_lines.append(msg)
        
        except TypeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Type Mismatch Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check return types - get_member() should return str, list_all_members() should return list"
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Review implementation for logic errors. Check method signatures match specification"
            print(msg)
            report_lines.append(msg)

    # ============ FINAL SCORING ============
    score_line = f"\nSCORE: {total_score}/{max_score} (Visible)"
    if total_score == 0:
        score_line += "\n⚠️ No tests passed. Make sure to implement all required methods with correct signatures."
    
    print(score_line)
    report_lines.append(score_line)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


def _setup_tc1(MembershipSystem):
    """TC1 Setup: Check names in blank system - Independent fresh instance."""
    return MembershipSystem()


def _setup_tc2(MembershipSystem):
    """TC2 Setup: Register two members - Independent fresh instance."""
    system = MembershipSystem()
    system.register_member("M101", "Alice")
    system.register_member("M102", "Bob")
    return system


def _setup_tc3(MembershipSystem):
    """TC3 Setup: Lookup existing member - Independent fresh instance."""
    system = MembershipSystem()
    system.register_member("M101", "Alice")
    system.register_member("M102", "Bob")
    return system


def _setup_tc4(MembershipSystem):
    """TC4 Setup: Lookup missing member - Independent fresh instance."""
    system = MembershipSystem()
    system.register_member("M101", "Alice")
    system.register_member("M102", "Bob")
    return system


def _setup_tc5(MembershipSystem):
    """TC5 Setup: Remove member and verify - Independent fresh instance."""
    system = MembershipSystem()
    system.register_member("M101", "Alice")
    system.register_member("M102", "Bob")
    system.remove_member("M101")
    return system


def _setup_tc6(MembershipSystem):
    """TC6 Setup: List names after removal - Independent fresh instance."""
    system = MembershipSystem()
    system.register_member("M101", "Alice")
    system.register_member("M102", "Bob")
    system.remove_member("M101")
    return system


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solution_path = sys.argv[1]
    else:
        solution_path = os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.py')
    test_student_code(solution_path)
