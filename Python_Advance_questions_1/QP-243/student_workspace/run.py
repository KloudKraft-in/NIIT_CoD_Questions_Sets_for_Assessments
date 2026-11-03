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
        from solution import PaginatedIterator
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # Mock Data Source
    def mock_db(offset, limit):
        mock_db.call_count += 1
        return list(range(offset, min(offset + limit, 25)))
    mock_db.call_count = 0

    # TC1: Initialization
    try:
        it1 = PaginatedIterator(mock_db, 10)
        if hasattr(it1, 'total_fetched'):
            results.append(("TC1", "Initialization", "Passed", 0))
        else:
            results.append(("TC1", "Initialization", "Failed", 0))
    except Exception as e:
        results.append(("TC1", "Initialization", f"Failed ({e})", 0))

    # TC2: Iterator Check
    try:
        it2 = PaginatedIterator(mock_db, 5)
        # Robustness: Force inject if __init__ is broken
        it2.fetch_func = mock_db
        it2.page_size = 5
        
        if iter(it2) is it2:
            results.append(("TC2", "Iterator Protocol", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Iterator Protocol", "Failed (iter() not self)", 0))
    except Exception as e:
        results.append(("TC2", "Iterator Protocol", f"Failed ({e})", 0))

    # TC3: Basic Yielding
    try:
        mock_db.call_count = 0
        it3 = PaginatedIterator(mock_db, 10)
        # Robustness
        it3.fetch_func = mock_db
        it3.page_size = 10
        if not hasattr(it3, 'buffer'): it3.buffer = []
        if not hasattr(it3, 'offset'): it3.offset = 0
        if not hasattr(it3, 'total_fetched'): it3.total_fetched = 0
        
        items = [next(it3) for _ in range(5)]
        if items == [0, 1, 2, 3, 4] and mock_db.call_count == 1:
            results.append(("TC3", "Sequential Access", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Sequential Access", f"Failed (Got {items}, count: {mock_db.call_count})", 0))
    except Exception as e:
        results.append(("TC3", "Sequential Access", f"Failed ({e})", 0))

    # TC4: Pagination Logic (Buffer handling)
    try:
        mock_db.call_count = 0
        it4 = PaginatedIterator(mock_db, 5)
        # Robustness
        it4.fetch_func = mock_db
        it4.page_size = 5
        it4.buffer = []
        it4.offset = 0
        
        # Fetch 5 (Call 1)
        for _ in range(5): next(it4)
        count_before = mock_db.call_count
        # This next call should trigger fetch (Call 2)
        next(it4)
        count_after = mock_db.call_count
        
        if count_before == 1 and count_after == 2:
            results.append(("TC4", "Batch Data Fetching", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC4", "Batch Data Fetching", f"Failed (Buffer logic incorrect: {count_before}->{count_after})", 0))
    except Exception as e:
        results.append(("TC4", "Batch Data Fetching", f"Failed ({e})", 0))

    # TC5: StopIteration Handling
    try:
        it5 = PaginatedIterator(mock_db, 10)
        # Robustness
        it5.fetch_func = mock_db
        it5.page_size = 10
        it5.buffer = []
        it5.offset = 0
        
        data = list(it5)
        if len(data) == 25 and data[-1] == 24:
            results.append(("TC5", "Full Data Exhaustion", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC5", "Full Data Exhaustion", f"Failed (Data length: {len(data)})", 0))
    except Exception as e:
        results.append(("TC5", "Full Data Exhaustion", f"Failed ({e})", 0))

    # TC6: Total Fetched Property
    try:
        mock_db.call_count = 0
        it6 = PaginatedIterator(mock_db, 10)
        # Robustness
        it6.fetch_func = mock_db
        it6.page_size = 10
        it6.offset = 0
        it6.buffer = []
        if hasattr(it6, '_total_fetched'):
            it6._total_fetched = 0
        
        next(it6) # Fetches first page
        if it6.total_fetched == 10:
             results.append(("TC6", "Total Fetched Tracking", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC6", "Total Fetched Tracking", f"Failed (Got {getattr(it6, 'total_fetched', 'N/A')})", 0))
    except Exception as e:
         results.append(("TC6", "Total Fetched Tracking", f"Failed ({e})", 0))

    # TC7: Specific Page Size
    try:
        def small_source(off, lim): return [off] if off < 3 else []
        it7 = PaginatedIterator(small_source, 1)
        # Robustness
        it7.fetch_func = small_source
        it7.page_size = 1
        it7.offset = 0
        it7.buffer = []
        
        data = list(it7)
        if data == [0, 1, 2]:
             results.append(("TC7", "Dynamic Offset Support", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC7", "Dynamic Offset Support", f"Failed (Got {data})", 0))
    except Exception as e:
         results.append(("TC7", "Dynamic Offset Support", f"Failed ({e})", 0))


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
        f.write(f"Paginated Iterator Assessment Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        for res in results:
            f.write(f"{res[0]}: {res[2]} ({res[3]} marks)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
