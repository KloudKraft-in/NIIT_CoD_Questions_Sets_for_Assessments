class SupplyChainInventory:

    def __init__(self):
        """Initialize an empty inventory dictionary."""
        self.stock = {}

    def add_product(self, product_id: str, quantity: int) -> dict:

        #your code here
        return self.stock

    def fulfill_order(self, product_id: str, quantity: int) -> dict:
        #your code here
        return self.stock

    def restock_return(self, product_id: str, quantity: int) -> dict:
        #your code here        
        return self.stock

    def list_available_products(self) -> list:
        #your code ehere
        return [product_id for product_id, qty in self.stock.items() if qty > 0]


