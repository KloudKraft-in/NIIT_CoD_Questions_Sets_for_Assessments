import numpy as np
import matplotlib.pyplot as plt

class SensorDataAnalytics:
    def __init__(self, raw_readings: list):
        # TODO: Initialize internal NumPy array self.data
        pass

    def sanitize_data(self, min_bound: float, max_bound: float) -> list:
        # TODO: Clip self.data within [min_bound, max_bound]
        return []

    def get_analysis_report(self) -> dict:
        # TODO: Return mean, median, std as dictionary
        return {}

    def normalize_readings(self) -> list:
        # TODO: Scale values to [0, 1]
        return []

    def detect_extreme_outliers(self, threshold_std: float) -> list:
        # TODO: Return indices of values > threshold_std from mean
        return []

    def calculate_moving_average(self, window_size: int) -> list:
        # TODO: Return simple rolling average list
        return []

    def compute_correlation(self, other_readings: list) -> float:
        # TODO: Compute Pearson Correlation Coefficient
        return 0.0

    def generate_sensor_line_chart(self, title: str):
        # TODO: Create line plot of self.data, set title/labels, return Figure
        pass

    def generate_frequency_histogram(self, bins: int):
        # TODO: Create histogram of self.data, set title/labels, return Figure
        pass

    def generate_correlation_scatter(self, other_readings: list):
        # TODO: Create scatter plot vs other_readings, return Figure
        pass
