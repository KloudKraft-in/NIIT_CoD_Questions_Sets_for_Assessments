import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
import json
from datetime import datetime

# Add current directory to sys.path to import solution.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def run_tests():
    print("-" * 50)
    print("TESTING SOLUTION: solution.py")
    print("-" * 50)
    
    try:
        from solution import Account, BankValidator, BankingError, InsufficientFundsError, LimitExceededError
    except ImportError as e:
        print(f"Error: Could not import classes from solution.py. {e}")
        return

    results = []
    total_marks = 0

    # TC1: Initialization
    try:
        bv_tc1 = BankValidator()
        if hasattr(bv_tc1, 'accounts') and isinstance(bv_tc1.accounts, dict) and len(bv_tc1.accounts) == 0:
            results.append(("TC1", "Initialization", "Passed", 0))
        else:
            results.append(("TC1", "Initialization", "Failed (Incorrect attributes)", 0))
    except Exception as e:
        results.append(("TC1", "Initialization", f"Failed ({e})", 0))

    # TC2: Create Account
    try:
        bv_tc2 = BankValidator()
        # Robustness: Force inject if __init__ is missing it
        if not hasattr(bv_tc2, 'accounts'):
            bv_tc2.accounts = {}
        
        msg = bv_tc2.create_account("A3", 5000.0, 2000.0)
        if msg == "Account A3 Created" and "A3" in bv_tc2.accounts:
            results.append(("TC2", "Account Storage", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC2", "Account Storage", "Failed (Incorrect return or storage)", 0))
    except Exception as e:
        results.append(("TC2", "Account Storage", f"Failed ({e})", 0))

    # TC3: Get Balance (Independent)
    try:
        bv_tc3 = BankValidator()
        # Direct Injection: Forcefully set/overwrite the accounts dict
        bv_tc3.accounts = {"A1": Account("A1", 1000.0, 500.0)}
        
        bal1 = bv_tc3.get_balance("A1")
        bal2 = bv_tc3.get_balance("NON_EXISTENT")
        if bal1 == 1000.0 and bal2 == -1.0:
            results.append(("TC3", "Balance Check", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC3", "Balance Check", f"Failed (Got {bal1}, {bal2})", 0))
    except Exception as e:
        results.append(("TC3", "Balance Check", f"Failed ({e})", 0))

    # TC4: Validate Transaction (Independent)
    try:
        bv_tc4 = BankValidator()
        # Direct Injection
        bv_tc4.accounts = {"A1": Account("A1", 1000.0, 500.0)}
        
        passed_checks = 0
        try:
            bv_tc4.validate_transaction("A1", 600.0) # > limit
        except LimitExceededError:
            passed_checks += 1
        
        try:
            bv_tc4.validate_transaction("A1", 1100.0) # > balance
        except InsufficientFundsError:
            passed_checks += 1
            
        if passed_checks == 2:
            results.append(("TC4", "Exception Triggers", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC4", "Exception Triggers", f"Failed (Checks passed: {passed_checks}/2)", 0))
    except Exception as e:
        results.append(("TC4", "Exception Triggers", f"Failed ({e})", 0))

    # TC5: Secure Withdrawal Flow (Independent)
    try:
        bv_tc5 = BankValidator()
        # Direct Injection
        bv_tc5.accounts = {
            "A1": Account("A1", 1000.0, 500.0),
            "A2": Account("A2", 300.0, 1000.0)
        }
        
        # Successful
        msg1 = bv_tc5.perform_withdrawal("A1", 400.0)
        # Error handling (Insufficient Funds)
        msg2 = bv_tc5.perform_withdrawal("A2", 400.0)
        
        if msg1 == "Withdrawal Successful" and bv_tc5.accounts["A1"].balance == 600.0 and "Insufficient" in msg2:
            results.append(("TC5", "Withdrawal Flow", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC5", "Withdrawal Flow", "Failed (Incorrect logic or return)", 0))
    except Exception as e:
        results.append(("TC5", "Withdrawal Flow", f"Failed ({e})", 0))

    # TC6: Count At-Risk (Independent)
    try:
        bv_tc6 = BankValidator()
        # Direct Injection
        bv_tc6.accounts = {
            "A1": Account("A1", 600.0, 500.0),
            "A2": Account("A2", 300.0, 500.0), # Risk
            "A3": Account("A3", 499.0, 500.0)  # Risk
        }
        
        risk_count = bv_tc6.count_at_risk_accounts()
        if risk_count == 2:
            results.append(("TC6", "Risk Analytics", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC6", "Risk Analytics", f"Failed (Got {risk_count}, expected 2)", 0))
    except Exception as e:
        results.append(("TC6", "Risk Analytics", f"Failed ({e})", 0))

    # TC7: Total bank balance (Independent)
    try:
        bv_tc7 = BankValidator()
        # Direct Injection
        bv_tc7.accounts = {
            "A1": Account("A1", 1000.0, 500.0),
            "A2": Account("A2", 500.0, 500.0)
        }
        
        total_bal = bv_tc7.get_total_bank_balance()
        if total_bal == 1500.0:
            results.append(("TC7", "Global Liquidity", "Passed", 5))
            total_marks += 5
        else:
            results.append(("TC7", "Global Liquidity", f"Failed (Got {total_bal}, expected 1500.0)", 0))
    except Exception as e:
        results.append(("TC7", "Global Liquidity", f"Failed ({e})", 0))


    # Display Results
    print(f"{'TC ID':<10} | {'Description':<25} | {'Status':<30} | {'Marks':<10}")
    print("-" * 85)
    for tcid, desc, status, marks in results:
        print(f"{tcid:<10} | {desc:<25} | {status:<30} | {marks:<10}")
    print("-" * 85)
    print(f"TOTAL MARKS: {total_marks} / 30")
    print("-" * 50)

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
        f.write(f"Banking Audit Report - {report_content['timestamp']}\n")
        f.write("=" * 40 + "\n")
        for res in report_content['results']:
            f.write(f"{res['tcid']}: {res['status']} ({res['marks']} marks)\n")
        f.write("=" * 40 + "\n")
        f.write(f"Final Score: {total_marks}/30\n")

if __name__ == "__main__":
    run_tests()
