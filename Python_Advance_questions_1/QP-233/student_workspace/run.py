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
        from solution import LRUCache, lru_cache_custom
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Initialization
    try:
        cache1 = LRUCache(5)
        if hasattr(cache1, 'capacity') and cache1.capacity == 5:
            results.append(("TC1", "LRUCache Initialization", "Passed", 0))
        else:
            results.append(("TC1", "LRUCache Initialization", "Failed", 0))
    except Exception as e:
        results.append(("TC1", "LRUCache Initialization", f"Failed ({e})", 0))

    # TC2: Basic Put/Get
    try:
        cache2 = LRUCache(2)
        # Robustness: Force inject if __init__ is missing it
        if not hasattr(cache2, 'capacity'): cache2.capacity = 2
        if not hasattr(cache2, 'cache'): cache2.cache = {}
        
        cache2.put("k1", "v1")
        if cache2.get("k1") == "v1" and cache2.get("k2") == -1:
            results.append(("TC2", "Basic Put/Get", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Basic Put/Get", "Failed", 0))
    except Exception as e:
        results.append(("TC2", "Basic Put/Get", f"Failed ({e})", 0))

    # TC3: Eviction Logic
    try:
        cache3 = LRUCache(2)
        # Robustness: Force inject
        cache3.capacity = 2
        if not hasattr(cache3, 'cache'): cache3.cache = {}
        
        cache3.put(1, "A") # [1]
        cache3.put(2, "B") # [1, 2]
        cache3.put(3, "C") # [2, 3], 1 is evicted
        if cache3.get(1) == -1 and cache3.get(2) == "B" and cache3.get(3) == "C":
            results.append(("TC3", "Oldest Eviction", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Oldest Eviction", "Failed", 0))
    except Exception as e:
        results.append(("TC3", "Oldest Eviction", f"Failed ({e})", 0))

    # TC4: MRU Update (Access moves to end)
    try:
        cache4 = LRUCache(2)
        # Robustness
        cache4.capacity = 2
        if not hasattr(cache4, 'cache'): cache4.cache = {}
        
        cache4.put(1, "A") # [1]
        cache4.put(2, "B") # [1, 2]
        cache4.get(1)       # [2, 1], 1 is now more recent
        cache4.put(3, "C") # [1, 3], 2 is evicted
        if cache4.get(2) == -1 and cache4.get(1) == "A":
             results.append(("TC4", "Access Update MRU", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC4", "Access Update MRU", "Failed", 0))
    except Exception as e:
        results.append(("TC4", "Access Update MRU", f"Failed ({e})", 0))

    # TC5: Decorator Success
    try:
        calls = []
        @lru_cache_custom(capacity=2)
        def mock_func(x):
            calls.append(x)
            return x * 2
        
        mock_func(10) # call 1
        mock_func(10) # cached
        if len(calls) == 1:
             results.append(("TC5", "Decorator Caching", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC5", "Decorator Caching", "Failed (Wait, it called twice?)", 0))
    except Exception as e:
        results.append(("TC5", "Decorator Caching", f"Failed ({e})", 0))

    # TC6: Decorator Eviction
    try:
        @lru_cache_custom(capacity=2)
        def evicted_func(x):
            evicted_func.count += 1
            return x
        evicted_func.count = 0
        
        evicted_func(1)
        evicted_func(2)
        evicted_func(3) # Evicts 1
        evicted_func(1) # Re-runs 1
        
        if evicted_func.count == 4:
             results.append(("TC6", "Decorator Eviction", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC6", "Decorator Eviction", f"Failed ({evicted_func.count} calls)", 0))
    except Exception as e:
        results.append(("TC6", "Decorator Eviction", f"Failed ({e})", 0))

    # TC7: Decorator Metadata
    try:
        @lru_cache_custom(5)
        def meta_func(x):
            """Original Doc"""
            pass
        if meta_func.__name__ == "meta_func" and meta_func.__doc__ and "Original Doc" in meta_func.__doc__:
             results.append(("TC7", "Decorator Metadata", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC7", "Decorator Metadata", "Failed", 0))
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
        f.write(f"LRU Cache Assessment Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
