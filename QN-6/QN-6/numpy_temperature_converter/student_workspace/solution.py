import numpy as np

def create_temperature_array(celsius_list: list) -> np.ndarray:
    return np.array(celsius_list, dtype=float)

def convert_to_fahrenheit(celsius_array: np.ndarray) -> np.ndarray:
    return np.round((celsius_array * 9 / 5) + 32, 1)

def calculate_average_temperature(celsius_array: np.ndarray) -> float:
    return round(np.mean(celsius_array), 1)

def categorize_temperature(celsius_array: np.ndarray) -> np.ndarray:
    categories = []
    for temp in celsius_array:
        if temp < 10:
            categories.append("Cold")
        elif 10 <= temp <= 25:
            categories.append("Moderate")
        else:
            categories.append("Hot")
    return np.array(categories)
