import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
import json
import time
from datetime import datetime

# Add current directory to sys.path to import solution.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    print("-" * 85)
    print("TESTING SOLUTION: solution.py")
    print("-" * 85)
    
    try:
        from solution import RateLimiter, rate_limited, RateLimitExceededError
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Initial Capacity Capping
    try:
        lim1 = RateLimiter(capacity=2, refill_rate=1.0)
        # Robustness: Force set internal state if __init__ is flaky
        if not hasattr(lim1, 'tokens'): lim1.tokens = 2
        if not hasattr(lim1, 'capacity'): lim1.capacity = 2
        
        c1 = lim1.consume()
        c2 = lim1.consume()
        c3 = lim1.consume()
        if c1 and c2 and not c3:
            results.append(("TC1", "Initial Burst", "Passed", 0))
        else:
            results.append(("TC1", "Initial Burst", f"Failed (C1:{c1}, C2:{c2}, C3:{c3})", 0))
    except Exception as e:
        results.append(("TC1", "Initial Burst", f"Failed ({e})", 0))

    # TC2: Custom Exception Check
    try:
        err = RateLimitExceededError("Rate limit exceeded - Try later")
        if isinstance(err, Exception) and str(err) == "Rate limit exceeded - Try later":
            results.append(("TC2", "Exception Type", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Exception Type", "Failed (Incorrect inheritance or message)", 0))
    except Exception as e:
        results.append(("TC2", "Exception Type", f"Failed ({e})", 0))

    # TC3: Refill Logic (1 token every 1s)
    try:
        lim3 = RateLimiter(capacity=1, refill_rate=1.0)
        # Robustness
        lim3.tokens = 1
        lim3.capacity = 1
        lim3.refill_rate = 1.0
        lim3.last_refill = time.time()
        
        lim3.consume() # tokens: 0
        time.sleep(1.1)
        # Should be able to consume after 1 second refill
        if lim3.consume():
            results.append(("TC3", "Refill Logic", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Refill Logic", "Failed (Wait 1s didn't refill)", 0))
    except Exception as e:
        results.append(("TC3", "Refill Logic", f"Failed ({e})", 0))

    # TC4: Capacity Limitation (Independent)
    try:
        lim4 = RateLimiter(capacity=2, refill_rate=100.0)
        # Robustness
        lim4.tokens = 0
        lim4.capacity = 2
        lim4.refill_rate = 100.0
        lim4.last_refill = time.time() - 10 # Force a large refill gap
        
        # After large gap, tokens should be refill logic -> capped at 2
        # We call consume() which should trigger refill
        lim4.consume() # 1st
        lim4.consume() # 2nd
        if not lim4.consume(): # 3rd call should fail (capacity 2)
             results.append(("TC4", "Capacity Capping", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC4", "Capacity Capping", "Failed (Exceeded capacity limit)", 0))
    except Exception as e:
        results.append(("TC4", "Capacity Capping", f"Failed ({e})", 0))

    # TC5: Decorator Output & Error Raising
    try:
        lim5 = RateLimiter(capacity=1, refill_rate=0.1)
        # Robustness
        lim5.tokens = 1
        lim5.capacity = 1
        lim5.refill_rate = 0.1
        
        @rate_limited(lim5)
        def limited_func(): return "DATA"
        
        limited_func() # Success (Consume 1 token)
        try:
            limited_func() # Failure (0 tokens)
            results.append(("TC5", "Decorator Exceptions", "Failed (No error raised)", 0))
        except RateLimitExceededError as e:
            if str(e) == "Rate limit exceeded - Try later":
                results.append(("TC5", "Decorator Exceptions", "Passed", 5))
                total_marks += 5
            else:
                results.append(("TC5", "Decorator Exceptions", f"Failed (Wrong message: {e})", 0))
        except Exception as e:
                results.append(("TC5", "Decorator Exceptions", f"Failed (Wrong exception: {type(e).__name__})", 0))
    except Exception as e:
        results.append(("TC5", "Decorator Exceptions", f"Failed ({e})", 0))

    # TC6: Multiple Shared Limiters
    try:
        lim6 = RateLimiter(capacity=2, refill_rate=0.1)
        # Robustness
        lim6.tokens = 2
        lim6.capacity = 2
        lim6.refill_rate = 0.1
        
        @rate_limited(lim6)
        def a(): pass
        @rate_limited(lim6)
        def b(): pass
        
        a()
        b()
        # 3rd call to either should fail
        try:
             a()
             results.append(("TC6", "Shared Limiter State", "Failed (Exceeded 2 calls)", 0))
        except RateLimitExceededError:
             results.append(("TC6", "Shared Limiter State", "Passed", 5))
             total_marks += 5
    except Exception as e:
        results.append(("TC6", "Shared Limiter State", f"Failed ({e})", 0))

    # TC7: Metadata preservation
    try:
        lim7 = RateLimiter(1,1)
        @rate_limited(lim7)
        def metadata_test():
             """Docs"""
             pass
        if metadata_test.__name__ == "metadata_test" and metadata_test.__doc__ and "Docs" in metadata_test.__doc__:
             results.append(("TC7", "Decorator Metadata", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC7", "Decorator Metadata", "Failed (Metadata lost)", 0))
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
        f.write(f"Token Bucket Assessment Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
