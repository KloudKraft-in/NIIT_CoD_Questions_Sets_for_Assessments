import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
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
        from solution import DatabaseSession, AuditManager, audit_log
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Initialization
    try:
        ds_tc1 = DatabaseSession("test_db")
        if hasattr(ds_tc1, 'db_name') and ds_tc1.db_name == "test_db":
            results.append(("TC1", "Class Initialization", "Passed", 0))
        else:
            results.append(("TC1", "Class Initialization", "Failed (Incorrect attributes)", 0))
    except Exception as e:
        results.append(("TC1", "Class Initialization", f"Failed ({e})", 0))

    # TC2: Context Manager Entry logic (Independent)
    try:
        ds_tc2 = DatabaseSession("entry_test")
        # ULTRA ROBUST: Force set state before method call
        ds_tc2.db_name = "entry_test"
        ds_tc2.is_open = False
        
        f = io.StringIO()
        with redirect_stdout(f):
             # Try calling __enter__ directly or via with
             ds_tc2.__enter__()
        
        output = f.getvalue()
        if ds_tc2.is_open == True and "Session Started: entry_test" in output:
            results.append(("TC2", "Context Manager Entry", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Context Manager Entry", f"Failed (Open: {getattr(ds_tc2, 'is_open', 'N/A')}, Output: {output.strip()})", 0))
    except Exception as e:
        results.append(("TC2", "Context Manager Entry", f"Failed ({e})", 0))

    # TC3: Context Manager Exit protection (Independent)
    try:
        ds_tc3 = DatabaseSession("exit_test")
        # ULTRA ROBUST: Force set state before method call
        ds_tc3.db_name = "exit_test"
        ds_tc3.is_open = True
        
        f = io.StringIO()
        with redirect_stdout(f):
            try:
                ds_tc3.__exit__(None, None, None)
            except:
                pass
        
        output = f.getvalue()
        if ds_tc3.is_open == False and "Session Ended: exit_test" in output:
            results.append(("TC3", "Context Manager Exit", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Context Manager Exit", f"Failed (Open: {getattr(ds_tc3, 'is_open', 'N/A')}, Output: {output.strip()})", 0))
    except Exception as e:
        results.append(("TC3", "Context Manager Exit", f"Failed ({e})", 0))

    # TC4: Decorator implementation (@audit_log) (Independent)
    try:
        @audit_log
        def independent_func(x):
            return x * 2
            
        f = io.StringIO()
        if independent_func is None:
             results.append(("TC4", "Decorator Logic", "Failed (Decorator returned None)", 0))
        else:
            with redirect_stdout(f):
                res = independent_func(5)
            output = f.getvalue()
            if res == 10 and "LOG: Starting independent_func" in output and "LOG: Finishing independent_func" in output:
                results.append(("TC4", "Decorator Logic", "Passed", 5))
                total_marks += 5
            else:
                results.append(("TC4", "Decorator Logic", "Failed (Incorrect output/return)", 0))
    except Exception as e:
        results.append(("TC4", "Decorator Logic", f"Failed ({e})", 0))

    # TC5: Decorated operation execution (Independent)
    try:
        am_tc5 = AuditManager()
        ds_tc5 = DatabaseSession("exec_test")
        ds_tc5.is_open = True
        ds_tc5.db_name = "exec_test"
        
        if not hasattr(am_tc5, 'execute_query') or am_tc5.execute_query is None:
             results.append(("TC5", "Decorated Operation", "Failed (Method missing/broken)", 0))
        else:
            f = io.StringIO()
            with redirect_stdout(f):
                res = am_tc5.execute_query(ds_tc5, "SELECT 1")
            output = f.getvalue()
            if res == "Success" and "LOG: Starting execute_query" in output:
                results.append(("TC5", "Decorated Operation", "Passed", 5))
                total_marks += 5
            else:
                results.append(("TC5", "Decorated Operation", "Failed", 0))
    except Exception as e:
        results.append(("TC5", "Decorated Operation", f"Failed ({e})", 0))

    # TC6: Context state validation (Independent)
    try:
        am_tc6 = AuditManager()
        # Mock session to avoid init issues
        class MockSession: pass
        ms = MockSession()
        
        ms.is_open = True
        res_true = am_tc6.session_integrity(ms)
        
        ms.is_open = False
        res_false = am_tc6.session_integrity(ms)
        
        if res_true == True and res_false == False:
            results.append(("TC6", "Context State Check", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC6", "Context State Check", f"Failed", 0))
    except Exception as e:
        results.append(("TC6", "Context State Check", f"Failed ({e})", 0))

    # TC7: static/Class variable tracking (Independent)
    try:
        # Resolve class variable name manually
        tracker = 'total_queries' if hasattr(AuditManager, 'total_queries') else 'query_count'
        setattr(AuditManager, tracker, 10)
        
        am_tc7 = AuditManager()
        if hasattr(am_tc7, 'get_query_count') and am_tc7.get_query_count() == 10:
             # Getter works independently of execution
             results.append(("TC7", "Class Variable Tracking", "Passed", 5))
             total_marks += 5
        else:
             results.append(("TC7", "Class Variable Tracking", "Failed", 0))
    except Exception as e:
        results.append(("TC7", "Class Variable Tracking", f"Failed ({e})", 0))



    # Display Results
    print(f"{'TC ID':<10} | {'Description':<25} | {'Status':<30} | {'Marks':<10}")
    print("-" * 85)
    for tcid, desc, status, marks in results:
        print(f"{tcid:<10} | {desc:<25} | {status:<30} | {marks:<10}")
    print("-" * 85)
    print(f"TOTAL MARKS: {total_marks} / 30")
    print("-" * 85)

    # Generate Report
    report_content = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_marks": total_marks,
        "results": [
            {"tcid": r[0], "description": r[1], "status": r[2], "marks": r[3]} for r in results
        ]
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.abspath(os.path.join(current_dir, "..", "reports"))
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"report_{timestamp}.txt"
    report_path = os.path.join(report_dir, report_filename)
    
    with open(report_path, "w") as f:
        f.write(f"Audit Session Manager Report - {report_content['timestamp']}\n")
        f.write("=" * 40 + "\n")
        for res in report_content['results']:
            f.write(f"{res['tcid']}: {res['status']} ({res['marks']} marks)\n")
        f.write("=" * 40 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
