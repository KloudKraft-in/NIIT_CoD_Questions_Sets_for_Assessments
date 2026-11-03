import importlib.util
import os
import sys
import random

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable."
    return True, None

# Embedded Reference Logic for Grading (Oracle)
class _GradingLogic:
    @staticmethod
    def get_reversed_itinerary(destinations):
        return [city.upper() for city in destinations[::-1]]

    @staticmethod
    def format_itinerary(destinations):
        if not destinations: return "No Destinations"
        joined = " -> ".join(destinations)
        return f"{joined} ({len(destinations)} stops)"

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

    print("Running Tests for: Travel Itinerary Planner (Professional Expansion)\n")
    report_lines = ["Running Tests for: Travel Itinerary Planner (Professional Expansion)\n"]

    if not hasattr(solution, "ItineraryPlanner"):
        msg = "ERROR: ItineraryPlanner class not found in solution.py"
        print(msg); report_lines.append(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")
        return

    # Randomized Seed for Hardcoding Prevention
    rv = random.randint(1, 100)
    base_cities = [f"City_{rv}", f"City_{rv+1}", f"City_{rv+2}"]

    test_cases = [
        {
            "desc": "Verification of list initialization",
            "func": "__init__",
            "setup": lambda: solution.ItineraryPlanner(base_cities),
            "call": lambda obj: obj.destinations,
            "check": lambda res: res == base_cities,
            "expected_output": f"Itinerary initialized with {base_cities}.",
            "marks": 0
        },
        {
            "desc": "Strategic adding of new destination",
            "func": "add_destination",
            "setup": lambda: solution.ItineraryPlanner(base_cities),
            "call": lambda obj: (obj.add_destination(base_cities[-1]), obj.add_destination(f"City_{rv+10}")),
            "check": lambda res: res == (False, True),
            "expected_output": "Sequential duplicate add returns False; unique city returns True.",
            "marks": 1
        },
        {
            "desc": "Number of unique stops in the plan",
            "func": "get_total_stops",
            "setup": lambda: solution.ItineraryPlanner(base_cities + [base_cities[0]]),
            "call": lambda obj: obj.get_total_stops(),
            "check": lambda res: res == len(set(base_cities)),
            "expected_output": f"Expected {len(set(base_cities))} unique stops.",
            "marks": 1
        },
        {
            "desc": "Finding the index of a specific stop",
            "func": "get_stop_index",
            "setup": lambda: solution.ItineraryPlanner(base_cities),
            "call": lambda obj: obj.get_stop_index(base_cities[1]),
            "check": lambda res: res == 1,
            "expected_output": "Index of second city should be 1.",
            "marks": 1
        },
        {
            "desc": "Removing a valid destination",
            "func": "remove_destination",
            "setup": lambda: solution.ItineraryPlanner(base_cities),
            "call": lambda obj: (obj.remove_destination(base_cities[0]), base_cities[0] in obj.destinations),
            "check": lambda res: res == (True, False),
            "expected_output": "First city removed successfully.",
            "marks": 1
        },
        {
            "desc": "Reversed itinerary in uppercase",
            "func": "get_reversed_itinerary",
            "setup": lambda: solution.ItineraryPlanner(base_cities),
            "call": lambda obj: obj.get_reversed_itinerary(),
            "check": lambda res: res == _GradingLogic.get_reversed_itinerary(base_cities),
            "expected_output": "List in reverse order and UPPERCASE.",
            "marks": 2
        },
        {
            "desc": "Detecting identical city names",
            "func": "has_duplicates",
            "setup": lambda: solution.ItineraryPlanner(base_cities + [base_cities[0]]),
            "call": lambda obj: obj.has_duplicates(),
            "check": lambda res: res == True,
            "expected_output": "Duplicate detected successfully.",
            "marks": 2
        },
        {
            "desc": "Formatting string with stop count",
            "func": "format_itinerary",
            "setup": lambda: solution.ItineraryPlanner(base_cities),
            "call": lambda obj: obj.format_itinerary(),
            "check": lambda res: res == _GradingLogic.format_itinerary(base_cities),
            "expected_output": "Formatted string with ' -> ' and stop count.",
            "marks": 2
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

    score_line = f"\nSCORE: {total_score}/10.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    sol_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
