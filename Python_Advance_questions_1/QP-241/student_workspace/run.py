import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
import json
import functools
from datetime import datetime

# Add current directory to sys.path to import solution.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    print("-" * 85)
    print("TESTING SOLUTION: solution.py")
    print("-" * 85)
    
    try:
        from solution import validate_schema
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Correct Execution on Valid
    try:
        @validate_schema({'val': int})
        def mock_func(**kwargs): return kwargs['val'] * 2
        
        # Robustness: Test simple valid case
        if mock_func(val=5) == 10:
            results.append(("TC1", "Valid Inputs Passed", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC1", "Valid Inputs Passed", "Failed", 0))
    except Exception as e:
         results.append(("TC1", "Valid Inputs Passed", f"Failed ({e})", 0))

    # TC2: Missing Argument logic
    try:
        # Robustness: Local definition for isolation
        @validate_schema({'id': int})
        def id_func(**kwargs): pass
        
        try:
             id_func() # No id provided
             results.append(("TC2", "Missing Arg Failure", "Failed (No error raised)", 0))
        except TypeError as e:
             if "Missing argument: id" in str(e):
                  results.append(("TC2", "Missing Arg Failure", "Passed", 5))
                  total_marks += 5
             else:
                  results.append(("TC2", "Missing Arg Failure", f"Failed (Wrong message: {e})", 0))
    except Exception as e:
        results.append(("TC2", "Missing Arg Failure", f"Failed ({e})", 0))

    # TC3: Incorrect Type logic
    try:
        # Robustness
        @validate_schema({'name': str})
        def name_func(**kwargs): pass
        
        try:
             name_func(name=123)
             results.append(("TC3", "Type Check Failure", "Failed (No error raised)", 0))
        except TypeError as e:
             msg = str(e)
             if "name must be" in msg and "got <class 'int'>" in msg:
                  results.append(("TC3", "Type Check Failure", "Passed", 5))
                  total_marks += 5
             else:
                  results.append(("TC3", "Type Check Failure", f"Failed (Wrong message formatting: {msg})", 0))
    except Exception as e:
         results.append(("TC3", "Type Check Failure", f"Failed ({e})", 0))

    # TC4: Multiple Validations
    try:
        # Robustness
        @validate_schema({'x': int, 'y': float, 'z': str})
        def multi(**kwargs): return "OK"
        
        if multi(x=1, y=2.5, z="test") == "OK":
             results.append(("TC4", "Multi-Field Validation", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC4", "Multi-Field Validation", "Failed", 0))
    except Exception as e:
         results.append(("TC4", "Multi-Field Validation", f"Failed ({e})", 0))

    # TC5: Allowance for Other Fields
    try:
        # Robustness
        @validate_schema({'status': bool})
        def extra(**kwargs): return kwargs.get('other', 'default')
        
        if extra(status=True, other='custom') == 'custom':
             results.append(("TC5", "Extra Field Allowance", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC5", "Extra Field Allowance", "Failed", 0))
    except Exception as e:
         results.append(("TC5", "Extra Field Allowance", f"Failed ({e})", 0))

    # TC6: Function Metadata Preservation
    try:
        # Robustness
        @validate_schema({})
        def actual_function():
             """Original Documentation"""
             pass
        
        if actual_function.__name__ == "actual_function" and actual_function.__doc__ == "Original Documentation":
             results.append(("TC6", "Metadata Integrity", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC6", "Metadata Integrity", "Failed (Wraps missing)", 0))
    except Exception as e:
        results.append(("TC6", "Metadata Integrity", f"Failed ({e})", 0))


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
        f.write(f"Schema Validation Assessment Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
