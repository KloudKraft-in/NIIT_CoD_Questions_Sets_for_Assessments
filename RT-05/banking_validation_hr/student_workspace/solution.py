from typing import List, Optional
import sys

# Complete the 'BankAccount' class below.
# Processes banking operations with custom validation rules.

class InsufficientFundsError(Exception):
    def __init__(self, message: str = "Insufficient funds"):
        # Implementation here
        pass        

class InvalidTransactionType(Exception):
    def __init__(self, message: str):
        # Implementation here
        pass

clas Transaction:
    def __init__(self, trans_type: str, amount: float, balance_after: float):
        # Implementation here
        pass

    def __str__(self) -> str:
        # Implementation here
        return ""

class BankAccount:
    def __init__(self, initial_balance: float = 1500.0):
        # Implementation here
        pass

    def process_transaction(self, trans_type: str, amount: float) -> str:
        # Implementation here
        return ""

    def get_transaction_history(self) -> List[str]:
        # Return list of transaction strings
        return []




#NOTE : Don't modify below code.
def process_banking_operations():
    try:
        input_data = sys.stdin.read().splitlines()
        if not input_data:
            return
            
        n = int(input_data[0].strip())
        account = BankAccount()
        line_idx = 1

        for _ in range(n):
            if line_idx >= len(input_data): break
            cmd = input_data[line_idx].strip()
            line_idx += 1
            if not cmd: continue
            
            if cmd == "view_transaction_history":
                for record in account.get_transaction_history():
                    print(record)
            elif cmd in ["deposit", "withdraw"]:
                if line_idx >= len(input_data): break
                amount = float(input_data[line_idx].strip())
                line_idx += 1
                print(account.process_transaction(cmd, amount))
            else:
                # Trigger invalid type error
                print(account.process_transaction(cmd, 0))

    except (InsufficientFundsError, InvalidTransactionType) as e:
        print(f"Error ({e.status_code}): {e}")
    except Exception as e:
        # Re-raise unexpected errors so they are visible
        raise e

if __name__ == '__main__':
    process_banking_operations()
