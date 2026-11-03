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
        from solution import Transaction, AuditorManager
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Initialization
    try:
        am_tc1 = AuditorManager()
        if hasattr(am_tc1, 'transactions') and isinstance(am_tc1.transactions, dict) and len(am_tc1.transactions) == 0:
            results.append(("TC1", "Initialization", "Passed", 0))
        else:
            results.append(("TC1", "Initialization", "Failed (Incorrect attributes)", 0))
    except Exception as e:
        results.append(("TC1", "Initialization", f"Failed ({e})", 0))

    # TC2: Add Transaction
    try:
        am_tc2 = AuditorManager()
        # Robustness: Force inject if __init__ is missing it
        if not hasattr(am_tc2, 'transactions'):
            am_tc2.transactions = {}
        
        msg = am_tc2.add_transaction("TXN5", 5500.0, "Verified")
        if msg == "Added TXN5" and "TXN5" in am_tc2.transactions:
            results.append(("TC2", "Add Transaction", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Add Transaction", "Failed (Incorrect return or storage)", 0))
    except Exception as e:
        results.append(("TC2", "Add Transaction", f"Failed ({e})", 0))

    # TC3: Get Transaction Amount (Independent)
    try:
        am_tc3 = AuditorManager()
        # Direct Injection: Forcefully set/overwrite the transactions dict
        am_tc3.transactions = {"TXN1": Transaction("TXN1", 6000.0, "Verified")}
        
        amt1 = am_tc3.get_txn_amount("TXN1")
        amt2 = am_tc3.get_txn_amount("NON_EXISTENT")
        if amt1 == 6000.0 and amt2 == 0.0:
            results.append(("TC3", "Get Amount", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Get Amount", f"Failed (Got {amt1}, {amt2})", 0))
    except Exception as e:
        results.append(("TC3", "Get Amount", f"Failed ({e})", 0))

    # TC4: Count by Status (Independent)
    try:
        am_tc4 = AuditorManager()
        # Direct Injection: Forcefully set the state
        am_tc4.transactions = {
            "T1": Transaction("T1", 1000.0, "Verified"),
            "T2": Transaction("T2", 2000.0, "Verified"),
            "T3": Transaction("T3", 3000.0, "Pending")
        }
        
        verified_count = am_tc4.count_by_status("Verified")
        if verified_count == 2:
            results.append(("TC4", "Status Filter", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC4", "Status Filter", f"Failed (Got {verified_count}, expected 2)", 0))
    except Exception as e:
        results.append(("TC4", "Status Filter", f"Failed ({e})", 0))

    # TC5: High-Value Streamer (Independent)
    try:
        import types
        am_tc5 = AuditorManager()
        # Direct Injection
        am_tc5.transactions = {
            "H1": Transaction("H1", 6000.0, "Verified"),
            "L1": Transaction("L1", 1500.0, "Verified"),
            "HP": Transaction("HP", 7000.0, "Pending")
        }
        
        gen = am_tc5.stream_high_value()
        is_gen = isinstance(gen, types.GeneratorType)
        yielded = list(gen) if is_gen else []
        yielded_ids = [t.txn_id for t in yielded]
        # Should only yield H1 (amount > 5000 and NOT Pending)
        if is_gen and set(yielded_ids) == {"H1"}:
            results.append(("TC5", "Generator Streamer", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC5", "Generator Streamer", f"Failed (Gen: {is_gen}, Yielded: {yielded_ids})", 0))
    except Exception as e:
        results.append(("TC5", "Generator Streamer", f"Failed ({e})", 0))

    # TC6: Count Flagged Pending (Independent)
    try:
        am_tc6 = AuditorManager()
        # Direct Injection
        am_tc6.transactions = {
            "P1": Transaction("P1", 7000.0, "Pending"),
            "P2": Transaction("P2", 3000.0, "Pending"),
            "V1": Transaction("V1", 8000.0, "Verified")
        }
        
        flagged = am_tc6.count_flagged_pending()
        if flagged == 1:
            results.append(("TC6", "Flagged Pending", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC6", "Flagged Pending", f"Failed (Got {flagged}, expected 1)", 0))
    except Exception as e:
        results.append(("TC6", "Flagged Pending", f"Failed ({e})", 0))

    # TC7: Audit Summary (Independent)
    try:
        am_tc7 = AuditorManager()
        # Direct Injection
        am_tc7.transactions = {
            "TXN1": Transaction("TXN1", 6000.0, "Verified"),
            "TXN2": Transaction("TXN2", 1500.0, "Verified"),
            "TXN3": Transaction("TXN3", 7000.0, "Pending")
        }
        
        summary = am_tc7.generate_audit_summary()
        expected = {'total': 3, 'high_value_yielded': 1}
        if summary == expected:
            results.append(("TC7", "Audit Summary", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC7", "Audit Summary", f"Failed (Got {summary})", 0))
    except Exception as e:
        results.append(("TC7", "Audit Summary", f"Failed ({e})", 0))


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
        f.write(f"Audit Report - {report_content['timestamp']}\n")
        f.write("=" * 40 + "\n")
        for res in report_content['results']:
            f.write(f"{res['tcid']}: {res['status']} ({res['marks']} marks)\n")
        f.write("=" * 40 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
