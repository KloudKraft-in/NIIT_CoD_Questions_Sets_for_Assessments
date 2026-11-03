import pandas as pd
import numpy as np

class SoilTempMonitor:
    """Soil Temperature Monitoring System using Pandas."""
    
    def __init__(self):
        """Initialize the SoilTempMonitor with an empty DataFrame."""
        self.df = None
    
    def read_data(self, file_path: str):
        """Load the CSV file into a Pandas DataFrame."""
        self.df = pd.read_csv(file_path)
    
    def clean_records(self) -> int:
        """Drop NaN rows in 'Temperature' and return count of dropped rows."""
        pass
    
    def find_highest_temp(self) -> int:
        """Return maximum temperature."""
        pass
    
    def sensor_averages(self) -> dict:
        """Return dict of {SensorID: mean_temperature} rounded to 2 decimal places."""
        pass
    
    def high_temp_sensors(self, threshold: int) -> list:
        """Return sorted list of unique SensorIDs above threshold."""
        pass
    
    def count_high_temp_sensors(self, threshold: int) -> int:
        """Return count of high-temperature sensors."""
        pass
