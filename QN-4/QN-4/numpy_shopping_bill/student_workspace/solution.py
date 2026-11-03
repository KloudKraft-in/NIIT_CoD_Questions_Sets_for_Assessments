import numpy as np

class ShoppingBillCalculator:
    def create_price_array(self, price_list):
        return np.array(price_list, dtype=float)

    def calculate_total_cost(self, price_array, quantity_array):
        return float(np.sum(price_array * quantity_array))

    def apply_discount(self, price_array, discount_percent):
        discount_factor = 1 - (discount_percent / 100)
        return price_array * discount_factor

    def filter_items_above_threshold(self, price_array, threshold):
        return price_array[price_array > threshold]