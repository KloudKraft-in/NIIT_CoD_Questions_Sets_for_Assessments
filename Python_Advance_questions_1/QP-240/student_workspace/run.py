import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
import json
import re
from datetime import datetime

# Add current directory to sys.path to import solution.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    print("-" * 85)
    print("TESTING SOLUTION: solution.py")
    print("-" * 85)
    
    try:
        from solution import LogForensics
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Named Groups Check (Attribute exist and works)
    try:
        lf1 = LogForensics()
        line = "2024-01-01 12:00:00 [DEBUG] Mod: Msg"
        res = lf1.parse_line(line)
        if isinstance(res, dict) and all(k in res for k in ['timestamp', 'level', 'component', 'message']):
            results.append(("TC1", "Regex Group Extraction", "Passed", 0))
        else:
            results.append(("TC1", "Regex Group Extraction", "Failed (Missing named groups)", 0))
    except Exception as e:
        results.append(("TC1", "Regex Group Extraction", f"Failed ({e})", 0))

    # TC2: Data Parsing Extraction
    try:
        lf2 = LogForensics()
        res = lf2.parse_line("2021-12-01 08:00:00 [CRITICAL] Core: System halted")
        if res['level'] == 'CRITICAL' and res['component'] == 'Core' and res['message'] == 'System halted':
            results.append(("TC2", "Parsing Accuracy", "Passed", 5))
            total_marks += 5
        else:
             results.append(("TC2", "Parsing Accuracy", "Failed", 0))
    except Exception as e:
        results.append(("TC2", "Parsing Accuracy", f"Failed ({e})", 0))

    # TC3: Invalid Line Resilience
    try:
        lf3 = LogForensics()
        res = lf3.parse_line("INVALID LOG")
        if res is None:
            results.append(("TC3", "Invalid Line Handling", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Invalid Line Handling", "Failed (Did not return None)", 0))
    except Exception as e:
        results.append(("TC3", "Invalid Line Handling", f"Failed ({e})", 0))

    # TC4: Log Processing
    try:
        lf4 = LogForensics()
        lf4.process_logs(["2020-01-01 00:00:00 [INFO] A: B", "trash", "2020-01-01 00:00:01 [WARN] C: D"])
        if len(lf4.logs) == 2:
            results.append(("TC4", "Batch Processing", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC4", "Batch Processing", f"Failed (Parsed {len(lf4.logs)} logs)", 0))
    except Exception as e:
        results.append(("TC4", "Batch Processing", f"Failed ({e})", 0))

    # TC5: Level Statistics
    try:
        lf5 = LogForensics()
        # Robustness: Force inject logs if process_logs is broken
        lf5.logs = [{'level': 'INFO'}, {'level': 'INFO'}, {'level': 'ERROR'}]
        stats = lf5.get_level_statistics()
        if stats == {'INFO': 2, 'ERROR': 1}:
            results.append(("TC5", "Level Statistics", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC5", "Level Statistics", f"Failed (Got: {stats})", 0))
    except Exception as e:
        results.append(("TC5", "Level Statistics", f"Failed ({e})", 0))

    # TC6: Component Report
    try:
        lf6 = LogForensics()
        # Robustness
        lf6.logs = [{'component': 'DB'}, {'component': 'API'}, {'component': 'DB'}]
        rpt = lf6.get_component_report()
        if rpt == {'DB': 2, 'API': 1}:
            results.append(("TC6", "Component Activity", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC6", "Component Activity", f"Failed (Got: {rpt})", 0))
    except Exception as e:
        results.append(("TC6", "Component Activity", f"Failed ({e})", 0))

    # TC7: Filtering by Component & Error
    try:
        lf7 = LogForensics()
        # Robustness
        lf7.logs = [
            {'level': 'ERROR', 'component': 'DB', 'message': 'M1'},
            {'level': 'INFO', 'component': 'DB', 'message': 'M2'},
            {'level': 'ERROR', 'component': 'NET', 'message': 'M3'}
        ]
        res = lf7.find_errors_by_component('DB')
        if res == ['M1']:
             results.append(("TC7", "Targeted Error Search", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC7", "Targeted Error Search", f"Failed (Got {res})", 0))
    except Exception as e:
         results.append(("TC7", "Targeted Error Search", f"Failed ({e})", 0))


    # Display Results
    print(f"{'TC ID':<10} | {'Description':<25} | {'Status':<30} | {'Marks':<10}")
    print("-" * 85)
    for tcid, desc, status, marks in results:
        print(f"{tcid:<10} | {desc:<25} | {status:<30} | {marks:<10}")
    print("-" * 85)
    print(f"TOTAL MARKS: {total_marks} / 30")
    print("-" * 85)

    # Generate Report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.abspath(os.path.join(current_dir, "..", "reports"))
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"report_{timestamp}.txt"
    report_path = os.path.join(report_dir, report_filename)
    
    with open(report_path, "w") as f:
        f.write(f"Log Forensics Assessment Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
