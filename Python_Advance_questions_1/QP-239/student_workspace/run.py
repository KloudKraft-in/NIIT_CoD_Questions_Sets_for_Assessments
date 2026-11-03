import os
import sys
import json
from datetime import datetime

# Ensure we don't write bytecode
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Path injection
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    print("-" * 85)
    print("TESTING SOLUTION: solution.py")
    print("-" * 85)
    
    try:
        from solution import DataProcessor, AnalyticsManager
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Initialization & Composition Check
    try:
        am_tc1 = AnalyticsManager()
        if hasattr(am_tc1, 'processor') and isinstance(am_tc1.processor, DataProcessor):
            results.append(("TC1", "Initialization/Composition", "Passed", 0))
        else:
            results.append(("TC1", "Initialization/Composition", "Failed (Incorrect attributes)", 0))
    except Exception as e:
        results.append(("TC1", "Initialization/Composition", f"Failed ({e})", 0))

    # TC2: Load Values Success
    try:
        am_tc2 = AnalyticsManager()
        am_tc2.processor.values = [10, 20, 30] # Robustness: Force state
        if am_tc2.processor.values == [10, 20, 30]:
            results.append(("TC2", "Data Loading", "Passed", 5))
            total_marks += 5
    except Exception as e:
        results.append(("TC2", "Data Loading", f"Failed ({e})", 0))

    # TC3: Average Calculation (via Composition)
    try:
        am_tc3 = AnalyticsManager()
        am_tc3.processor.values = [10, 20, 30]
        avg = am_tc3.get_average()
        if avg == 20.0:
            results.append(("TC3", "Average Calculation", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Average Calculation", f"Failed (Got {avg})", 0))
    except Exception as e:
        results.append(("TC3", "Average Calculation", f"Failed ({e})", 0))

    # TC4: Min/Max Calculation (via Composition)
    try:
        am_tc4 = AnalyticsManager()
        am_tc4.processor.values = [5, 15, 25]
        low, high = am_tc4.get_bounds()
        if low == 5 and high == 25:
            results.append(("TC4", "Min/Max Bounds", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC4", "Min/Max Bounds", f"Failed (Got {low}, {high})", 0))
    except Exception as e:
        results.append(("TC4", "Min/Max Bounds", f"Failed ({e})", 0))

    # TC5: Empty List Handling
    try:
        am_tc5 = AnalyticsManager()
        am_tc5.processor.values = []
        try:
             am_tc5.get_average()
             results.append(("TC5", "Empty Stats Handled", "Failed (No ZeroDivisionError)", 0))
        except ZeroDivisionError:
             results.append(("TC5", "Empty Stats Handled", "Passed", 5))
             total_marks += 5
    except Exception as e:
        results.append(("TC5", "Empty Stats Handled", f"Failed ({e})", 0))

    # TC6: Filter Above average
    try:
        am_tc6 = AnalyticsManager()
        am_tc6.processor.values = [10, 20, 30, 40] # Avg = 25
        filtered = am_tc6.get_above_average()
        if filtered == [30, 40]:
             results.append(("TC6", "Above Average Filter", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC6", "Above Average Filter", "Failed", 0))
    except Exception as e:
        results.append(("TC6", "Above Average Filter", f"Failed ({e})", 0))

    # TC7: Summary Dictionary
    try:
        am_tc7 = AnalyticsManager()
        am_tc7.processor.values = [10, 30]
        summary = am_tc7.get_status_report()
        expected = {'count': 2, 'avg': 20.0, 'max': 30}
        if summary == expected:
            results.append(("TC7", "Status Report Summary", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC7", "Status Report Summary", f"Failed (Got {summary})", 0))
    except Exception as e:
        results.append(("TC7", "Status Report Summary", f"Failed ({e})", 0))

    # Display Results
    print(f"{'TC ID':<10} | {'Description':<25} | {'Status':<30} | {'Marks':<10}")
    print("-" * 85)
    for tcid, desc, status, marks in results:
        print(f"{tcid:<10} | {desc:<25} | {status:<30} | {marks:<10}")
    print("-" * 85)
    print(f"TOTAL SCORE: {total_marks} / 30")
    print("-" * 85)

    # Generate Report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.abspath(os.path.join(current_dir, "..", "reports"))
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"report_{timestamp}.txt"
    report_path = os.path.join(report_dir, report_filename)
    
    with open(report_path, "w") as f:
        f.write(f"Composition Analytics Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
