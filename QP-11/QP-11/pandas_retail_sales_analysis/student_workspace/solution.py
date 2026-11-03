# solution.py
import pandas as pd

class RetailSalesAnalyzer:

    def load_transactions(self, file_path: str) -> pd.DataFrame:
        """
        Loads a CSV file and returns it as a Pandas DataFrame.
        """
        return pd.read_csv(file_path)

    def total_purchase_value(self, df: pd.DataFrame) -> float:
        """
        Calculates total sales value from quantity * unit_price.
        This function works independently and does not modify the original DataFrame.
        """
        df_copy = df.copy()
        df_copy["revenue"] = df_copy["quantity"] * df_copy["unit_price"]
        return df_copy["revenue"].sum()

    def top_product_category(self, df: pd.DataFrame) -> tuple:
        """
        Finds the top-selling category by revenue.
        This function works independently and does not modify the original DataFrame.
        """
        df_copy = df.copy()
        df_copy["revenue"] = df_copy["quantity"] * df_copy["unit_price"]
        category_revenue = df_copy.groupby("product_category")["revenue"].sum()
        top = category_revenue.sort_values(ascending=False).head(1)
        return (top.index[0], float(top.values[0]))

    def top_n_products(self, df: pd.DataFrame) -> list:
        """
        Returns a list of top 3 products sold by quantity.
        """
        df_copy = df.copy()
        product_quantity = df_copy.groupby("product_name")["quantity"].sum()
        top_3 = product_quantity.sort_values(ascending=False).head(3)
        return [(product, int(quantity)) for product, quantity in top_3.items()]
