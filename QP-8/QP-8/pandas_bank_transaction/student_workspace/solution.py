# student_workspace/solution.py

import pandas as pd

class BankTransactionAnalyzer:
    def load_transactions(self, file_path: str) -> pd.DataFrame:
        """
        Load the transaction data from the given CSV file.
        Returns a DataFrame with columns: customer_id, type, amount, date
        """
        return pd.read_csv(file_path)

    def total_by_type(self, df: pd.DataFrame) -> dict:
        """
        Calculate total credited and debited amounts from the DataFrame.
        Returns:
            dict: {"credit": <total>, "debit": <total>}
        """
        credit_total = df[df["type"] == "credit"]["amount"].sum()
        debit_total = df[df["type"] == "debit"]["amount"].sum()
        return {
            "credit": float(credit_total),
            "debit": float(debit_total)
        }

    def high_value_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return all transactions where amount > 10000.
        Returns:
            pd.DataFrame: Filtered transactions
        """
        return df[df["amount"] > 10000].reset_index(drop=True)

    def top_customers(self, df: pd.DataFrame) -> list:
        """
        Return the top 3 customers by total transaction amount.
        Returns:
            list: [(customer_id, total_amount), ...]
        """
        totals = df.groupby("customer_id")["amount"].sum()
        top = totals.sort_values(ascending=False).head(3)
        return [(int(cust_id), float(amount)) for cust_id, amount in top.items()]