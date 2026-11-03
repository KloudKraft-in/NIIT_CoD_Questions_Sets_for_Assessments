import pandas as pd
import numpy as np

class SoilTempMonitor:
    """
    Soil Temperature Monitoring System using Pandas.
    Manages soil sensor data with efficient DataFrame operations.
    """
    
    def __init__(self):
        """Initialize the SoilTempMonitor with an empty DataFrame."""
        self.df = None
    
    def read_data(self, file_path: str):
        """Load the CSV file into a Pandas DataFrame."""
        self.df = pd.read_csv(file_path)
    
    def clean_records(self) -> int:
        """Drop all rows where 'Temperature' is NaN."""
        if self.df is None: return 0
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['Temperature'])
        return initial_count - len(self.df)
    
    def find_highest_temp(self) -> int:
        """Find the maximum temperature in the dataset."""
        if self.df is None or self.df.empty: return 0
        return int(self.df["Temperature"].max())
    
    def sensor_averages(self) -> dict:
        """Calculate mean 'Temperature' for each 'SensorID'."""
        if self.df is None or self.df.empty: return {}
        return self.df.groupby("SensorID")["Temperature"].mean().round(2).to_dict()
    
    def high_temp_sensors(self, threshold: int) -> list:
        """Return sorted list of unique SensorIDs above threshold."""
        if self.df is None or self.df.empty: return []
        high_temp_sns = self.df[self.df["Temperature"] > threshold]["SensorID"].unique().tolist()
        return sorted(high_temp_sns)
    
    def count_high_temp_sensors(self, threshold: int) -> int:
        """Count unique sensors with temperature above threshold."""
        return len(self.high_temp_sensors(threshold))
