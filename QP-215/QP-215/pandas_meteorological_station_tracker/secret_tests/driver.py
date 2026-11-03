import importlib.util
import os
import sys
import pandas as pd
import random

def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable."
    return True, None

# Embedded Reference Logic for Grading (QP-221 Style)
class _GradingLogic:
    @staticmethod
    def is_heatwave(df_r, city):
        return any(df_r[df_r['City'] == city]['Temp'] > 40)

    @staticmethod
    def get_rain_summary(df_r, city):
        data = df_r[df_r['City'] == city]
        if data.empty: return "No Data."
        avg = data['Rain'].mean()
        if avg > 100: return "Heavy Rain"
        if avg > 50: return "Moderate"
        return "Light"

    @staticmethod
    def get_wettest_city(df_r):
        return df_r.groupby('City')['Rain'].sum().idxmax()

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

    print("Running Tests for: Meteorological Station (Professional Edition)\n")
    report_lines = ["Running Tests for: Meteorological Station (Professional Edition)\n"]

    if not hasattr(solution, "WeatherManager"):
        msg = "ERROR: WeatherManager class not found in solution.py"
        print(msg); report_lines.append(msg)
        with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")
        return

    # Data Paths
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    readings_p = os.path.join(data_dir, "weather_readings.csv")
    stations_p = os.path.join(data_dir, "city_stations.csv")
    
    try:
        raw_readings = pd.read_csv(readings_p)
        raw_stations = pd.read_csv(stations_p)
        merged_ref = pd.merge(raw_readings, raw_stations, on="City")
    except Exception as e:
        print(f"CRITICAL ERROR: Data missing. {e}"); return

    def compare_rounded(r, e, precision=1):
        try:
            if isinstance(r, (float, int)): return round(float(r), precision) == round(float(e), precision)
            if isinstance(r, dict):
                return all(compare_rounded(r[k], e.get(k)) for k in e)
            if isinstance(r, list):
                return sorted(str(x) for x in r) == sorted(str(y) for y in e)
            return str(r) == str(e)
        except: return False

    test_cases = [
        {
            "desc": "Initialize and Load internal DataFrames",
            "func": "load_data",
            "setup": lambda: solution.WeatherManager(),
            "call": lambda obj: (obj.load_data(readings_p, stations_p), isinstance(obj.df_readings, pd.DataFrame)),
            "check": lambda res: res[1] == True,
            "expected_output": "WeatherManager.df_readings should be a DataFrame after loading.",
            "marks": 0
        },
        {
            "desc": "Verify Inner Join merging logic",
            "func": "get_merged_data",
            "setup": lambda: _inject_data(solution.WeatherManager(), raw_readings, raw_stations),
            "call": lambda obj: obj.get_merged_data(),
            "check": lambda res: len(res) == len(merged_ref) and 'Temp' in res.columns,
            "expected_output": "Merged DataFrame count should match inner join count.",
            "marks": 3
        },
        {
            "desc": "Heatwave check (Column Threshold > 40C)",
            "func": "is_heatwave",
            "setup": lambda: solution.ClimateProcessor(),
            "call": lambda obj: obj.is_heatwave(raw_readings, "Ahmedabad"),
            "check": lambda res: res == True,
            "expected_output": "True if Temp > 40 in records.",
            "marks": 3
        },
        {
            "desc": "Rainfall Intensity Summarization",
            "func": "get_rain_summary",
            "setup": lambda: solution.ClimateProcessor(),
            "call": lambda obj: obj.get_rain_summary(raw_readings, "Mumbai"),
            "check": lambda res: res == "Heavy Rain",
            "expected_output": "Heavy Rain if avg(Rain) > 100.",
            "marks": 3
        },
        {
            "desc": "Calculated overall average temperature",
            "func": "average_temp",
            "setup": lambda: solution.ClimateProcessor(),
            "call": lambda obj: obj.average_temp(raw_readings),
            "check": lambda res: compare_rounded(res, raw_readings['Temp'].mean()),
            "expected_output": "Overall mean temperature calculation for all cities.",
            "marks": 3
        },
        {
            "desc": "Detailed City Climate Dict",
            "func": "get_city_report",
            "setup": lambda: solution.ClimateProcessor(),
            "call": lambda obj: obj.get_city_report(raw_readings, "Jaipur"),
            "check": lambda res: isinstance(res, dict) and res.get('max_temp') == 43.0,
            "expected_output": "Dict with max_temp, min_temp, and total_rain.",
            "marks": 4
        },
        {
            "desc": "Wettest city identification (Sum Rain)",
            "func": "get_wettest_city",
            "setup": lambda: solution.ClimateProcessor(),
            "call": lambda obj: obj.get_wettest_city(raw_readings),
            "check": lambda res: res == _GradingLogic.get_wettest_city(raw_readings),
            "expected_output": "Name of city with highest cumulative rainfall.",
            "marks": 4
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

    score_line = f"\nSCORE: {total_score}/20.0"
    print(score_line); report_lines.append(score_line)
    with open(report_path, "w", encoding="utf-8") as f: f.write("\n".join(report_lines) + "\n")

def _inject_data(obj, r, s):
    obj.df_readings = r.copy(); obj.df_stations = s.copy()
    return obj

if __name__ == "__main__":
    sol_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(sol_file)
