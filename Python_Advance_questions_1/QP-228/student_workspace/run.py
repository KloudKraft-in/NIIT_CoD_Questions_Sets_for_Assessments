import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
import json
from datetime import datetime

# Add current directory to sys.path to import solution.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    print("-" * 85)
    print("TESTING SOLUTION: solution.py")
    print("-" * 85)
    
    try:
        from solution import CircuitOpenError, circuit_breaker
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Custom Exception Check
    try:
        err = CircuitOpenError("Test")
        if isinstance(err, Exception) and str(err) == "Test":
            results.append(("TC1", "Custom Exception", "Passed", 0))
        else:
            results.append(("TC1", "Custom Exception", "Failed (Incorrect inheritance or message)", 0))
    except Exception as e:
        results.append(("TC1", "Custom Exception", f"Failed ({e})", 0))

    # TC2: Successful Call (0 Failures)
    try:
        # Local definition for independence
        @circuit_breaker(failure_threshold=2)
        def func_ok(): return True
        
        if func_ok() is True:
            results.append(("TC2", "Success Reset", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Success Reset", "Failed", 0))
    except Exception as e:
        results.append(("TC2", "Success Reset", f"Failed ({e})", 0))

    # TC3: Failure Counting
    try:
        @circuit_breaker(failure_threshold=3)
        def func_fail(): raise ValueError("Fail")
        
        try: func_fail()
        except ValueError: pass
        
        # Test if another call can still go through (failure count is 1)
        try: 
            func_fail()
            # If we reached here, it means it didn't trip yet (correct)
            results.append(("TC3", "Failure Counting", "Passed", 5))
            total_marks += 5
        except ValueError:
            results.append(("TC3", "Failure Counting", "Passed", 5))
            total_marks += 5
        except CircuitOpenError:
            results.append(("TC3", "Failure Counting", "Failed (Tripped too early)", 0))
    except Exception as e:
        results.append(("TC3", "Failure Counting", f"Failed ({e})", 0))

    # TC4: Circuit Tripping (Tripped State)
    try:
        @circuit_breaker(failure_threshold=2)
        def func_tripper(): raise RuntimeError("Fatal")
        
        try: func_tripper()
        except: pass
        try: func_tripper()
        except: pass
        
        # Third call should raise CircuitOpenError
        try:
            func_tripper()
            results.append(("TC4", "Circuit Tripping", "Failed (Did not trip)", 0))
        except CircuitOpenError as e:
            if "OPEN" in str(e).upper():
                results.append(("TC4", "Circuit Tripping", "Passed", 5))
                total_marks += 5
            else:
                results.append(("TC4", "Circuit Tripping", f"Failed (Wrong error message: {e})", 0))
        except Exception as e:
            results.append(("TC4", "Circuit Tripping", f"Failed (Wrong exception: {type(e).__name__})", 0))
    except Exception as e:
        results.append(("TC4", "Circuit Tripping", f"Failed ({e})", 0))

    # TC5: Consecutive vs Reset (Success resets fail count)
    try:
        @circuit_breaker(failure_threshold=2)
        def func_adaptive(fail: bool):
            if fail: raise Exception("Fail")
            return "OK"
        
        try: func_adaptive(True)
        except: pass
        
        func_adaptive(False) # This should reset the count to 0
        
        try: 
            func_adaptive(True) # This is now the 1st failure again
            # Should not trip after this one failure
            res = func_adaptive(False)
            if res == "OK":
                results.append(("TC5", "Reset Logic", "Passed", 5))
                total_marks += 5
            else:
                results.append(("TC5", "Reset Logic", f"Failed (Got {res})", 0))
        except Exception as e:
             if isinstance(e, CircuitOpenError):
                 results.append(("TC5", "Reset Logic", "Failed (Incorrectly tripped)", 0))
             else:
                 results.append(("TC5", "Reset Logic", f"Failed ({e})", 0))
    except Exception as e:
        results.append(("TC5", "Reset Logic", f"Failed ({e})", 0))

    # TC6: Independent Circuit Breakers
    try:
        @circuit_breaker(failure_threshold=2)
        def service_a(): raise Exception("A")
        @circuit_breaker(failure_threshold=2)
        def service_b(): return "B"
        
        try: service_a(); service_a()
        except: pass
        
        # service_a should be OPEN, but service_b should be CLOSED
        try:
            res_b = service_b()
            if res_b == "B":
                results.append(("TC6", "State Isolation", "Passed", 5))
                total_marks += 5
            else:
                results.append(("TC6", "State Isolation", "Failed", 0))
        except CircuitOpenError:
            results.append(("TC6", "State Isolation", "Failed (Polluted state)", 0))
    except Exception as e:
        results.append(("TC6", "State Isolation", f"Failed ({e})", 0))

    # TC7: Metadata preservation
    try:
        @circuit_breaker(failure_threshold=2)
        def important_func():
            """Docs"""
            return True
        if important_func.__name__ == "important_func" and important_func.__doc__ and "Docs" in important_func.__doc__:
            results.append(("TC7", "Decorator Metadata", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC7", "Decorator Metadata", "Failed (Metadata not preserved)", 0))
    except Exception as e:
        results.append(("TC7", "Decorator Metadata", f"Failed ({e})", 0))


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
        f.write(f"Circuit Breaker Assessment Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
