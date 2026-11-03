# student_workspace/solution.py

class SavingsAccount:
    """
    Savings Account Manager using Object-Oriented Programming.
    Manages account holder information and balance operations.
    """
    
    def __init__(self, holder_name: str, initial_balance: float):
        """
        Initialize a savings account with holder name and initial balance.
        
        Parameters:
            holder_name (str): Name of the account holder
            initial_balance (float): Initial account balance
        """
        """ YOUR CODE HERE """
    
    def deposit(self, amount: float):
        """
        Deposit an amount into the account.
        
        Parameters:
            amount (float): Amount to deposit (increases balance)
        """
        """ YOUR CODE HERE """
    
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw an amount from the account if sufficient funds exist.
        
        Parameters:
            amount (float): Amount to withdraw
        
        Returns:
            bool: True if withdrawal successful, False if insufficient funds
        """
        """ YOUR CODE HERE """
    
    def get_balance(self) -> float:
        """
        Get the current account balance.
        """
        """ YOUR CODE HERE """
    
    def get_summary(self) -> str:
        """
        Get formatted account summary.
        
        Returns:
            str: Formatted string with holder name and balance
        """
        """ YOUR CODE HERE """

