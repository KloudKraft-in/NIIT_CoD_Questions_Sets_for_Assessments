import pandas as pd
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
    except ImportError as e:
        error_msg = f"IMPORT ERROR: {str(e)}\nMake sure pandas is imported correctly in solution.py"
        print(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        return
    
    print("Running Tests for: Ride Sharing Trip Analytics System\n")
    report_lines = ["Running Tests for: Ride Sharing Trip Analytics System\n"]
    
    # Verify class exists
    if not hasattr(solution, "RideSharingAnalytics"):
        error_msg = "ERROR: RideSharingAnalytics class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return
    
    RideSharingAnalytics = solution.RideSharingAnalytics
    
    # Get the data path
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    trips_csv = os.path.join(data_dir, 'trips.csv')
    
    test_cases = [
        {
            "desc": "TC1: Calculate revenue per city",
            "func": "revenue_by_city",
            "setup": lambda: _setup_basic(RideSharingAnalytics, trips_csv),
            "call": lambda obj: obj.revenue_by_city(),
            "check": lambda result: isinstance(result, dict) and 'Mumbai' in result and 'Pune' in result and 'Delhi' in result,
            "expected_output": "{'Mumbai': 410, 'Pune': 730, 'Delhi': 920}",
            "marks": 4
        },
        {
            "desc": "TC2: Find highest earning driver",
            "func": "highest_earning_driver",
            "setup": lambda: _setup_basic(RideSharingAnalytics, trips_csv),
            "call": lambda obj: obj.highest_earning_driver(),
            "check": lambda result: isinstance(result, tuple) and result[0] == 'D03' and result[1] == 920,
            "expected_output": "('D03', 920)",
            "marks": 4
        },
        {
            "desc": "TC3: Average distance per vehicle type",
            "func": "avg_distance_by_vehicle",
            "setup": lambda: _setup_basic(RideSharingAnalytics, trips_csv),
            "call": lambda obj: obj.avg_distance_by_vehicle(),
            "check": lambda result: isinstance(result, dict) and 'Mini' in result and 'Sedan' in result and 'SUV' in result and 'Auto' in result,
            "expected_output": "{'Mini': 6.67, 'Sedan': 10.0, 'SUV': 12.7, 'Auto': 3.2}",
            "marks": 4
        },
        {
            "desc": "TC4: Find peak demand hour",
            "func": "peak_demand_hour",
            "setup": lambda: _setup_basic(RideSharingAnalytics, trips_csv),
            "call": lambda obj: obj.peak_demand_hour(),
            "check": lambda result: isinstance(result, int) and result == 9,
            "expected_output": "9",
            "marks": 4
        },
        {
            "desc": "TC5: Detect trips with surge pricing",
            "func": "surge_trips",
            "setup": lambda: _setup_basic(RideSharingAnalytics, trips_csv),
            "call": lambda obj: obj.surge_trips(),
            "check": lambda result: isinstance(result, list) and set(result) == {'T102', 'T104', 'T107'},
            "expected_output": "['T102', 'T104', 'T107']",
            "marks": 4
        }
    ]

    total_score = 0
    max_score = 0

    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 4)
        max_score += marks
        
        try:
            # Verify method exists
            method_exists, error_msg = validate_method_exists(RideSharingAnalytics(), case["func"])
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
                msg += f"  Hint: Review the method implementation and data processing logic"
            
            print(msg)
            report_lines.append(msg)
        
        except FileNotFoundError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: File Not Found\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Make sure trips.csv exists in the data folder"
            print(msg)
            report_lines.append(msg)
        
        except AttributeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Attribute Not Found\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check the method implementation - ensure DataFrame operations are correct"
            print(msg)
            report_lines.append(msg)
        
        except TypeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Type Mismatch Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check method return types match specification"
            print(msg)
            report_lines.append(msg)
        
        except ValueError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Value Error\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Check your data processing logic"
            print(msg)
            report_lines.append(msg)
        
        except Exception as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: {type(e).__name__}\n"
            msg += f"  Details: {str(e)}\n"
            msg += f"  Hint: Review implementation for logic errors"
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


def _setup_basic(RideSharingAnalytics, trips_csv):
    """Setup for basic tests."""
    analytics = RideSharingAnalytics()
    analytics.read_data(trips_csv)
    return analytics


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solution_path = sys.argv[1]
    else:
        solution_path = os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.py')
    test_student_code(solution_path)
