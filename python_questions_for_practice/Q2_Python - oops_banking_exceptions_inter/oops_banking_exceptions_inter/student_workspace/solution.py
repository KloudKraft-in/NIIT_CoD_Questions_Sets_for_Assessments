# # Custom Exceptions
# class BankingError(Exception):
#     pass

# class InsufficientFundsError(BankingError):
#     # TODO: Implement base or custom logic if needed
#     pass

# class LimitExceededError(BankingError):
#     # TODO: Implement base or custom logic if needed
#     pass

# class Account:
#     def __init__(self, acc_id: str, balance: float, limit: float):
#         # TODO: Initialize attributes
#         pass

# class BankValidator:
#     def __init__(self):
#         # TODO: Initialize self.accounts as empty dict
#         pass

#     def create_account(self, acc_id: str, balance: float, limit: float) -> str:
#         # TODO: Store Account and return "Account [acc_id] Created"
#         pass

#     def get_balance(self, acc_id: str) -> float:
#         # TODO: Return balance or -1.0 if not found
#         pass

#     def validate_transaction(self, acc_id: str, amount: float):
#         # TODO: Check withdrawal constraints and raise InsufficientFundsError or LimitExceededError
#         pass

#     def perform_withdrawal(self, acc_id: str, amount: float) -> str:
#         # TODO: Call validate_transaction and update balance if successful
#         # Return "Withdrawal Successful" or catch exception and return its message
#         pass

#     def count_at_risk_accounts(self) -> int:
#         # TODO: Return count of accounts where balance < 500
#         pass

#     def get_total_bank_balance(self) -> float:
#         # TODO: Return sum of all balances
#         pass

class BankingError(Exception):
    pass

class InsufficientFundsError(BankingError):
    def __init__(self, message="Insufficient funds for withdrawal"):
        # self.message = message
        # super().__init__(self.message)
        pass
class LimitExceededError(BankingError):
    def __init__(self, message="Daily withdrawal limit exceeded"):
        # self.message = message
        # super().__init__(self.message)
        pass
class Account:
    def __init__(self, acc_id: str, balance: float, limit: float):
        # self.acc_id = acc_id
        # self.balance = balance
        # self.limit = limit
        pass
class BankValidator:
    def __init__(self):
        # self.accounts = {}
        pass
    def create_account(self, acc_id: str, balance: float, limit: float) -> str:
        self.accounts[acc_id] = Account(acc_id, balance, limit)
        return f"Account {acc_id} Created"
        pass
    def get_balance(self, acc_id: str) -> float:
        if acc_id in self.accounts:
            return self.accounts[acc_id].balance
        return -1.0
        pass

    def validate_transaction(self, acc_id: str, amount: float):
        # Validate and raise exceptions
        acc = self.accounts.get(acc_id)
        if not acc:
            return

        if amount > acc.balance:
            raise InsufficientFundsError(f"Insufficient funds for withdrawal")
        
        if amount > acc.limit:
            raise LimitExceededError(f"Daily withdrawal limit exceeded")

    def perform_withdrawal(self, acc_id: str, amount: float) -> str:
        # Check rules
        try:
            self.validate_transaction(acc_id, amount)
            acc = self.accounts[acc_id]
            acc.balance -= amount
            return "Withdrawal Successful"
        except (InsufficientFundsError, LimitExceededError) as e:
            # Catch exceptions and return the error message string
            return str(e)

    def count_at_risk_accounts(self) -> int:
        count = 0
        for acc in self.accounts.values():
            if acc.balance < 500:
                count += 1
        return count

    def get_total_bank_balance(self) -> float:
        total = 0.0
        for acc in self.accounts.values():
            total += acc.balance
        return total
