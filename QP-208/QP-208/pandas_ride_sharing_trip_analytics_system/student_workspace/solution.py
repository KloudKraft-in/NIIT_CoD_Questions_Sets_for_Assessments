# student_workspace/solution.py

import pandas as pd
import numpy as np

class RideSharingAnalytics:
    """
    Ride Sharing Trip Analytics System using Pandas.
    Analyzes trip data from a ride-hailing platform.
    """
    
    def __init__(self):
        """Initialize the RideSharingAnalytics with an empty DataFrame."""
        self.df = None
    
    def read_data(self, file_path: str):
        """
        Load the CSV file into a Pandas DataFrame.
        
        Parameters:
            file_path (str): Path to the CSV file
        """
        self.df = pd.read_csv(file_path)
    
    def revenue_by_city(self) -> dict:
        """
        Calculate total revenue generated per city.
        
        Returns:
            dict: Dictionary with city as key and total revenue as value
        """
        if self.df is None or self.df.empty:
            return {}
        
        revenue = self.df.groupby('city')['fare_amount'].sum().to_dict()
        return revenue
    
    def highest_earning_driver(self) -> tuple:
        """
        Identify the driver with the highest total earnings.
        
        Returns:
            tuple: (driver_id, total_earnings)
        """
        if self.df is None or self.df.empty:
            return (None, 0)
        
        driver_earnings = self.df.groupby('driver_id')['fare_amount'].sum()
        highest_driver = driver_earnings.idxmax()
        highest_earnings = driver_earnings.max()
        
        return (highest_driver, int(highest_earnings))
    
    def avg_distance_by_vehicle(self) -> dict:
        """
        Compute average trip distance grouped by vehicle type.
        
        Returns:
            dict: Dictionary with vehicle type as key and average distance as value (rounded to 2 decimals)
        """
        if self.df is None or self.df.empty:
            return {}
        
        avg_distance = self.df.groupby('vehicle_type')['distance_km'].mean().round(2).to_dict()
        return avg_distance
    
    def peak_demand_hour(self) -> int:
        """
        Determine peak demand hour using trip frequency analysis.
        
        Returns:
            int: Hour with highest trip count
        """
        if self.df is None or self.df.empty:
            return None
        
        hour_counts = self.df['start_hour'].value_counts()
        peak_hour = hour_counts.idxmax()
        
        return int(peak_hour)
    
    def surge_trips(self) -> list:
        """
        Detect trips where surge pricing was applied (surge_multiplier > 1).
        
        Returns:
            list: List of trip IDs with surge pricing applied
        """
        if self.df is None or self.df.empty:
            return []
        
        surge_df = self.df[self.df['surge_multiplier'] > 1.0]
        surge_trip_ids = surge_df['trip_id'].tolist()
        
        return surge_trip_ids
