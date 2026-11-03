import importlib.util
import os
import sys
import numpy as np

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

    print("Running Tests for: Weather Tracker\n")
    report_lines = ["Running Tests for: Weather Tracker\n"]

    # Verify class exists
    if not hasattr(student_module, "WeatherTracker"):
        error_msg = "ERROR: WeatherTracker class not found in solution.py"
        print(error_msg)
        report_lines.append(error_msg)
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        return

    test_cases = [
        {
            "desc": "Initialize WeatherTracker with empty arrays",
            "func": "initialize",
            "setup": lambda: student_module.WeatherTracker(),
            "call": lambda obj: (isinstance(obj.temperatures, np.ndarray), len(obj.temperatures)),
            "check": lambda result: result[0] and result[1] == 0,
            "expected_output": "Empty numpy arrays initialized",
            "marks": 5
        },
        {
            "desc": "Add temperature data",
            "func": "add_temperature_data",
            "setup": lambda: student_module.WeatherTracker(),
            "call": lambda obj: (obj.add_temperature_data([25.5, 26.0, 24.8]), obj.temperatures),
            "check": lambda result: result[0] is not None and isinstance(result[1], np.ndarray) and len(result[1]) == 3,
            "expected_output": "Method returns temperature array with 3 values and updates self.temperatures",
            "marks": 5
        },
        {
            "desc": "Calculate average temperature",
            "func": "calculate_average_temperature",
            "setup": lambda: _setup_temps(student_module),
            "call": lambda obj: obj.calculate_average_temperature(),
            "check": lambda result: abs(result - 25.43) < 0.01,
            "expected_output": "Average temperature = 25.43",
            "marks": 5
        },
        {
            "desc": "Get days above temperature threshold",
            "func": "get_days_above_temperature",
            "setup": lambda: _setup_temps_threshold(student_module),
            "call": lambda obj: len(obj.get_days_above_temperature(25.0)),
            "check": lambda result: result == 3,
            "expected_output": "3 temperatures above 25.0",
            "marks": 5
        },
        {
            "desc": "Get weather statistics",
            "func": "get_weather_statistics",
            "setup": lambda: _setup_stats(student_module),
            "call": lambda obj: obj.get_weather_statistics(),
            "check": lambda result: result.get('min_temp') == 24.8 and result.get('max_temp') == 26.0 and result.get('data_points') == 3,
            "expected_output": "Dictionary with min, max, avg, data_points",
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
                method_exists, error_msg = validate_method_exists(student_module.WeatherTracker(), case["func"])
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
        
        except AttributeError as e:
            msg = f"FAIL TC{idx} [{case['desc']}]\n"
            msg += f"  Error Type: Attribute Error\n"
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


def _setup_temps(student_module):
    """Setup for calculate_average_temperature test."""
    tracker = student_module.WeatherTracker()
    tracker.temperatures = np.array([25.5, 26.0, 24.8])
    return tracker


def _setup_temps_threshold(student_module):
    """Setup for get_days_above_temperature test."""
    tracker = student_module.WeatherTracker()
    tracker.temperatures = np.array([25.5, 26.0, 24.8, 27.2])
    return tracker


def _setup_stats(student_module):
    """Setup for get_weather_statistics test."""
    tracker = student_module.WeatherTracker()
    tracker.temperatures = np.array([25.5, 26.0, 24.8])
    return tracker


if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
