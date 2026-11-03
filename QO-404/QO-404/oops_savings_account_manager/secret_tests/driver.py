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
    
    print("Running Tests for: Savings Account Manager\n")
    report_lines = ["Running Tests for: Savings Account Manager\n"]
    
    # Verify class exists
    if not hasattr(solution, "SavingsAccount"):
        error_msg = "ERROR: SavingsAccount class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return
    
    SavingsAccount = solution.SavingsAccount
    
    test_cases = [
        {
            "desc": "Initialize account and check initial balance",
            "func": "get_balance",
            "setup": lambda: _setup_tc1(SavingsAccount),
            "call": lambda obj: obj.get_balance(),
            "check": lambda result: result == 1000.0,
            "expected_output": "Initial balance should be 1000.0",
            "marks": 2
        },
        {
            "desc": "Deposit 500 and verify new balance",
            "func": "deposit",
            "setup": lambda: _setup_tc2(SavingsAccount),
            "call": lambda obj: obj.get_balance(),
            "check": lambda result: result == 1500.0,
            "expected_output": "Balance after deposit should be 1500.0",
            "marks": 2
        },
        {
            "desc": "Withdraw 200 (Successful) and check balance",
            "func": "withdraw",
            "setup": lambda: _setup_tc3(SavingsAccount),
            "call": lambda obj: (obj.withdraw(200), obj.get_balance()),
            "check": lambda result: result == (True, 1300.0),
            "expected_output": "Withdraw should return True and balance should be 1300.0",
            "marks": 2
        },
        {
            "desc": "Withdraw 2000 (Insufficient funds)",
            "func": "withdraw",
            "setup": lambda: _setup_tc4(SavingsAccount),
            "call": lambda obj: (obj.withdraw(2000), obj.get_balance()),
            "check": lambda result: result == (False, 1300.0),
            "expected_output": "Withdraw should return False and balance should remain 1300.0",
            "marks": 2
        },
        {
            "desc": "Check formatted account summary string",
            "func": "get_summary",
            "setup": lambda: _setup_tc5(SavingsAccount),
            "call": lambda obj: obj.get_summary(),
            "check": lambda result: result == "Holder: Alice, Balance: 1300",
            "expected_output": "Summary should be 'Holder: Alice, Balance: 1300'",
            "marks": 2
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2)
        max_score += marks
        
        try:
            # Verify method exists
            method_exists, error_msg = validate_method_exists(SavingsAccount("TestHolder", 100), case["func"])
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
                msg += f"  Hint: Review the method implementation and data types"
            
            print(msg)
            report_lines.append(msg)
        
        except AttributeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Attribute Not Found\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check the method implementation - ensure attributes are correctly initialized"
            print(msg)
            report_lines.append(msg)
        
        except TypeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Type Mismatch Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check method return types - withdraw() should return bool, get_balance() should return float, get_summary() should return str"
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


def _setup_tc1(SavingsAccount):
    """TC1 Setup: Initialize account and check initial balance - Independent fresh instance."""
    return SavingsAccount("Alice", 1000)


def _setup_tc2(SavingsAccount):
    """TC2 Setup: Deposit 500 and verify new balance - Independent fresh instance."""
    account = SavingsAccount("Alice", 1000)
    account.deposit(500)
    return account


def _setup_tc3(SavingsAccount):
    """TC3 Setup: Withdraw 200 (Successful) - Independent fresh instance."""
    account = SavingsAccount("Alice", 1000)
    account.deposit(500)
    return account


def _setup_tc4(SavingsAccount):
    """TC4 Setup: Withdraw 2000 (Insufficient funds) - Independent fresh instance."""
    account = SavingsAccount("Alice", 1000)
    account.deposit(500)
    account.withdraw(200)
    return account


def _setup_tc5(SavingsAccount):
    """TC5 Setup: Check formatted account summary string - Independent fresh instance."""
    account = SavingsAccount("Alice", 1000)
    account.deposit(500)
    account.withdraw(200)
    return account


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solution_path = sys.argv[1]
    else:
        solution_path = os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.py')
    test_student_code(solution_path)
