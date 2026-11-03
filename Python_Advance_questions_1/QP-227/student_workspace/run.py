import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
import json
import io
from contextlib import redirect_stdout
from datetime import datetime

# Add current directory to sys.path to import solution.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    print("-" * 85)
    print("TESTING SOLUTION: solution.py")
    print("-" * 85)
    
    try:
        from solution import RetryManager, retryable
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Initialization & Global State
    try:
        RetryManager._enabled = True # Robustness: Force set internal state
        if RetryManager.isEnabled() is True:
            results.append(("TC1", "Initial State", "Passed", 0))
        else:
            results.append(("TC1", "Initial State", "Failed (Incorrect default)", 0))
    except Exception as e:
        results.append(("TC1", "Initial State", f"Failed ({e})", 0))

    # TC2: Set/Get Logic
    try:
        RetryManager.setEnabled(False)
        state1 = RetryManager.isEnabled()
        RetryManager.setEnabled(True)
        state2 = RetryManager.isEnabled()
        if state1 is False and state2 is True:
            results.append(("TC2", "Enabled/Disabled Flow", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Enabled/Disabled Flow", f"Failed (Got {state1}, {state2})", 0))
    except Exception as e:
        results.append(("TC2", "Enabled/Disabled Flow", f"Failed ({e})", 0))

    # TC3: Retry Success (First Attempt)
    try:
        RetryManager._enabled = True # Robustness
        f = io.StringIO()
        with redirect_stdout(f):
            @retryable(maxRetries=3)
            def simple_task():
                return "Completed"
            res = simple_task()
            output = f.getvalue().strip()
            
            if res == "Completed" and output == "":
                 results.append(("TC3", "Immediate Success", "Passed", 5))
                 total_marks += 5
            else:
                 results.append(("TC3", "Immediate Success", f"Failed (Output: {output})", 0))
    except Exception as e:
        results.append(("TC3", "Immediate Success", f"Failed ({e})", 0))

    # TC4: Retry Recovery (Second Attempt)
    try:
        RetryManager._enabled = True # Robustness
        f = io.StringIO()
        with redirect_stdout(f):
            def counter_func():
                counter_func.calls = getattr(counter_func, 'calls', 0) + 1
                if counter_func.calls == 1:
                    raise Exception("First Fail")
                return "Success"
            
            wrapped = retryable(maxRetries=3)(counter_func)
            res = wrapped()
            output = f.getvalue().strip()
            
            if res == "Success" and "Attempt 1 failed" in output and "Success after 2 attempts" in output:
                results.append(("TC4", "Recovery logic (1 retry)", "Passed", 5))
                total_marks += 5
            else:
                 results.append(("TC4", "Recovery logic (1 retry)", f"Failed (Output: {output})", 0))
    except Exception as e:
        results.append(("TC4", "Recovery logic (1 retry)", f"Failed ({e})", 0))

    # TC5: Max Retry Failure
    try:
        RetryManager._enabled = True # Robustness
        f = io.StringIO()
        with redirect_stdout(f):
            @retryable(maxRetries=2)
            def always_fail():
                raise ValueError("Fatal Error")
            
            try:
                always_fail()
                failed_to_raise = True
            except ValueError:
                failed_to_raise = False
            
            output = f.getvalue().strip()
            if not failed_to_raise and "Attempt 2 failed" in output and "ERROR: all retries failed" in output:
                 results.append(("TC5", "Max Attempts Handled", "Passed", 5))
                 total_marks += 5
            else:
                 results.append(("TC5", "Max Attempts Handled", f"Failed (Output: {output})", 0))
    except Exception as e:
        results.append(("TC5", "Max Attempts Handled", f"Failed ({e})", 0))

    # TC6: Disabled Override (Independent)
    try:
        RetryManager._enabled = False # Robustness: Force disable
        f = io.StringIO()
        with redirect_stdout(f):
            @retryable(maxRetries=10)
            def test_disabled():
                return "OK"
            res = test_disabled()
            output = f.getvalue().strip()
            if "Retry disabled" in output and res == "OK":
                 results.append(("TC6", "Disabled Override", "Passed", 5))
                 total_marks += 5
            else:
                 results.append(("TC6", "Disabled Override", f"Failed (Output: {output})", 0))
    except Exception as e:
        results.append(("TC6", "Disabled Override", f"Failed ({e})", 0))

    # TC7: Decorator Integrity (Independent)
    try:
        @retryable(maxRetries=3)
        def named_function():
            """This is a docstring"""
            return True
        
        if named_function.__name__ == "named_function" and named_function.__doc__ == "This is a docstring":
             results.append(("TC7", "Decorator wraps check", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC7", "Decorator wraps check", "Failed (Meta not preserved)", 0))
    except Exception as e:
        results.append(("TC7", "Decorator wraps check", f"Failed ({e})", 0))


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
        f.write(f"Automatic Retry Assessment Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
