import importlib.util
import os
import sys

def _setup_account(solution, aid, pin, bal, log):
    acc = solution.Account(aid, pin, bal)
    acc.acc_id = aid; acc.pin = pin; acc.balance = bal; acc.transaction_log = log
    return acc

def run_tests(solution_path=None):
    if solution_path is None:
        solution_path = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(solution)
    except Exception as e:
        print(f"IMPORT ERROR: {e}"); return

    if not hasattr(solution, "GlobalBankingSystem"):
        print("ERROR: GlobalBankingSystem class not found."); return

    test_cases = [
        {"desc": "Instantiate complex structures", "func": "__init__", "m": 0},
        {"desc": "Register account with initial log", "func": "create_account", "m": 1},
        {"desc": "Deposit with log tracking", "func": "deposit_funds", "m": 2},
        {"desc": "Withdrawal with -500 Overdraft logic", "func": "secure_withdraw", "m": 3},
        {"desc": "Retrieve full audit trail of account", "func": "get_transaction_history", "m": 1},
        {"desc": "Calculate total liquidity (net)", "func": "total_liquidity", "m": 1},
        {"desc": "Perform bulk interest sweep", "func": "apply_annual_interest", "m": 2}
    ]

    total_score = 0
    print("Running Local Evaluation for: Global Banking System\n")

    for idx, case in enumerate(test_cases, 1):
        marks = int(case["m"])
        desc = case["desc"]
        try:
            bank = solution.GlobalBankingSystem()
            has_init_state = hasattr(bank, 'accounts')
            if not has_init_state: bank.accounts = {}

            p_ok = False
            if idx == 1: 
                p_ok = has_init_state and isinstance(bank.accounts, dict)
            elif idx == 2: 
                p_ok = (bank.create_account("A1", 1, 100.0) == "Account A1 registered." and "A1" in bank.accounts)
            elif idx == 3: 
                bank.accounts["A1"] = _setup_account(solution, "A1", 1, 1000.0, ["Init"])
                p_ok = (bank.deposit_funds("A1", 500.0) == "Success. Balance: $1500.0" and bank.accounts["A1"].balance == 1500.0)
            elif idx == 4: 
                bank.accounts["A1"] = _setup_account(solution, "A1", 1, 1000.0, ["Init"])
                p_ok = (bank.secure_withdraw("A1", 1, 1800.0) == "Overdraft limit exceeded.")
            elif idx == 5: 
                bank.accounts["A1"] = _setup_account(solution, "A1", 1, 100.0, ["L1", "L2"])
                p_ok = (bank.get_transaction_history("A1") == ["L1", "L2"])
            elif idx == 6: 
                bank.accounts = {
                    "A1": _setup_account(solution, "A1", 1, 100.0, []),
                    "A2": _setup_account(solution, "A2", 1, -50.0, [])
                }
                p_ok = (bank.total_liquidity() == 50.0)
            elif idx == 7: 
                bank.accounts = {
                    "A1": _setup_account(solution, "A1", 1, 6000.0, []),
                    "A2": _setup_account(solution, "A2", 1, 1000.0, [])
                }
                p_ok = (bank.apply_annual_interest() == 1 and bank.accounts["A1"].balance == 6300.0)

            if p_ok: 
                total_score += marks
                print(f"PASS TC{idx} [{desc}] ({marks}/{marks})")
            else: 
                print(f"FAIL TC{idx} [{desc}] (0/{marks})")
        except Exception as e:
            print(f"FAIL TC{idx} [{desc}] (0/{marks}) | Error: {e}")

    print(f"\nSCORE: {total_score}/10 (Visible) | {total_score}/10 (Total)")

if __name__ == "__main__":
    run_tests()
