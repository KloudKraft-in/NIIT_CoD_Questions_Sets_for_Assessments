import pandas as pd
import numpy as np

class HealthMonitor:
    """
    Health Monitoring System using Pandas.
    Manages patient health data with efficient DataFrame operations.
    """
    
    def __init__(self):
        """Initialize the HealthMonitor with an empty DataFrame."""
        self.df = None
    
    def read_data(self, file_path: str):
        """Load the CSV file into a Pandas DataFrame."""
        self.df = pd.read_csv(file_path)
    
    def clean_records(self) -> int:
        """Drop all rows where 'HeartRate' is NaN."""
        if self.df is None: return 0
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['HeartRate'])
        return initial_count - len(self.df)
    
    def find_highest_rate(self) -> int:
        """Find the maximum heart rate in the dataset."""
        if self.df is None or self.df.empty: return 0
        return int(self.df["HeartRate"].max())
    
    def patient_averages(self) -> dict:
        """Calculate mean 'HeartRate' for each 'PatientID'."""
        if self.df is None or self.df.empty: return {}
        return self.df.groupby("PatientID")["HeartRate"].mean().round(2).to_dict()
    
    def high_risk(self, threshold: int) -> list:
        """Return sorted list of unique PatientIDs above threshold."""
        if self.df is None or self.df.empty: return []
        high_risk_pts = self.df[self.df["HeartRate"] > threshold]["PatientID"].unique().tolist()
        return sorted(high_risk_pts)
    
    def count_high_risk(self, threshold: int) -> int:
        """Count unique patients with heart rate above threshold."""
        return len(self.high_risk(threshold))
