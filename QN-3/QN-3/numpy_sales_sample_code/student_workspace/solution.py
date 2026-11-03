import numpy as np

def create_sales_array(sales_data: list) -> np.ndarray:
    # Convert the list to a NumPy array
    return np.array(sales_data)

def validate_sales_array(sales_array: np.ndarray) -> bool:
    # Check that the array is not empty and contains no negative values
    if sales_array.size == 0:
        return False
    for value in sales_array:
        if value < 0:
            return False
    return True

def compute_sales_metrics(sales_array: np.ndarray) -> tuple:
    # Return total sales, average sales, and max sales
    total = sales_array.sum()
    average = sales_array.mean()
    maximum = sales_array.max()
    return (total, average, maximum)

def categorize_demand_levels(sales_array: np.ndarray) -> np.ndarray:
    # Categorize sales levels based on value
    labels = []
    for sale in sales_array:
        if sale < 100:
            labels.append("Low Demand")
        elif 100 <= sale <= 250:
            labels.append("Moderate Demand")
        else:
            labels.append("High Demand")
    return np.array(labels)

def longest_growth_streak(sales_array: np.ndarray) -> int:
    # Return the length of the longest strictly increasing contiguous subarray
    if sales_array.size == 0:
        return 0

    max_streak = 1
    current_streak = 1

    for i in range(1, len(sales_array)):
        if sales_array[i] > sales_array[i - 1]:
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
        else:
            current_streak = 1

    return max_streak

def format_sales_data(sales_array: np.ndarray) -> np.ndarray:
    # Format each sales number with commas (e.g., 1000 -> "1,000")
    formatted = []
    for sale in sales_array:
        formatted.append(f"{sale:,}")
    return np.array(formatted)
