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
        from solution import ConfigMerger, MergeConflictError
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Initialization
    try:
        cm_tc1 = ConfigMerger()
        results.append(("TC1", "Initialization", "Passed", 0))
    except Exception as e:
        results.append(("TC1", "Initialization", f"Failed ({e})", 0))

    # TC2: Simple Merge (Non-nested)
    try:
        cm_tc2 = ConfigMerger()
        d1 = {"a": 1}
        d2 = {"b": 2}
        res = cm_tc2.merge(d1, d2)
        if res == {"a": 1, "b": 2}:
            results.append(("TC2", "Simple Merge", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Simple Merge", "Failed", 0))
    except Exception as e:
        results.append(("TC2", "Simple Merge", f"Failed ({e})", 0))

    # TC3: Nested Merge Success
    try:
        cm_tc3 = ConfigMerger()
        d1 = {"db": {"host": "localhost"}}
        d2 = {"db": {"port": 5432}}
        res = cm_tc3.merge(d1, d2)
        if res == {"db": {"host": "localhost", "port": 5432}}:
            results.append(("TC3", "Nested Merge Success", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Nested Merge Success", "Failed", 0))
    except Exception as e:
        results.append(("TC3", "Nested Merge Success", f"Failed ({e})", 0))

    # TC4: Deep Copy Verification
    try:
        cm_tc4 = ConfigMerger()
        d1 = {"x": [1]}
        d2 = {"y": 2}
        res = cm_tc4.merge(d1, d2)
        res["x"].append(2)
        if d1["x"] == [1]: # Original should not change
            results.append(("TC4", "Deep Copy Check", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC4", "Deep Copy Check", "Failed (Original modified)", 0))
    except Exception as e:
        results.append(("TC4", "Deep Copy Check", f"Failed ({e})", 0))

    # TC5: Conflict Detection (Value vs Dict)
    try:
        cm_tc5 = ConfigMerger()
        d1 = {"key": {"nested": 1}}
        d2 = {"key": 2}
        try:
            cm_tc5.merge(d1, d2)
            results.append(("TC5", "Conflict: Value/Dict", "Failed (No error raised)", 0))
        except MergeConflictError:
            results.append(("TC5", "Conflict: Value/Dict", "Passed", 5))
            total_marks += 5
    except Exception as e:
        results.append(("TC5", "Conflict: Value/Dict", f"Failed ({e})", 0))

    # TC6: Conflict Detection (Value vs Value)
    try:
        cm_tc6 = ConfigMerger()
        d1 = {"a": 1}
        d2 = {"a": 2}
        try:
            cm_tc6.merge(d1, d2)
            results.append(("TC6", "Conflict: Value/Value", "Failed (No error raised)", 0))
        except MergeConflictError:
            results.append(("TC6", "Conflict: Value/Value", "Passed", 5))
            total_marks += 5
    except Exception as e:
        results.append(("TC6", "Conflict: Value/Value", f"Failed ({e})", 0))

    # TC7: Complex Deep Merge
    try:
        cm_tc7 = ConfigMerger()
        d1 = {"app": {"settings": {"theme": "dark"}}}
        d2 = {"app": {"settings": {"font": "Arial"}}}
        res = cm_tc7.merge(d1, d2)
        if res == {"app": {"settings": {"theme": "dark", "font": "Arial"}}}:
            results.append(("TC7", "Complex Deep Merge", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC7", "Complex Deep Merge", f"Failed (Got {res})", 0))
    except Exception as e:
        results.append(("TC7", "Complex Deep Merge", f"Failed ({e})", 0))

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
        f.write(f"Recursive Dict Merger Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
