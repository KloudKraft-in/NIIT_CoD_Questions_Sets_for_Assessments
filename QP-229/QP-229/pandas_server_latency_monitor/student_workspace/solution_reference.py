import pandas as pd
import numpy as np

class ServerLatencyMonitor:
    """
    Server Latency Monitoring System using Pandas.
    Manages server latency logs with efficient DataFrame operations.
    """
    
    def __init__(self):
        """Initialize the ServerLatencyMonitor with an empty DataFrame."""
        self.df = None
    
    def read_data(self, file_path: str):
        """Load the CSV file into a Pandas DataFrame."""
        self.df = pd.read_csv(file_path)
    
    def clean_records(self) -> int:
        """Drop all rows where 'Latency' is NaN."""
        if self.df is None: return 0
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['Latency'])
        return initial_count - len(self.df)
    
    def find_highest_latency(self) -> int:
        """Find the maximum latency in the dataset."""
        if self.df is None or self.df.empty: return 0
        return int(self.df["Latency"].max())
    
    def endpoint_averages(self) -> dict:
        """Calculate mean 'Latency' for each 'EndpointID'."""
        if self.df is None or self.df.empty: return {}
        return self.df.groupby("EndpointID")["Latency"].mean().round(2).to_dict()
    
    def high_latency_endpoints(self, threshold: int) -> list:
        """Return sorted list of unique EndpointIDs above threshold."""
        if self.df is None or self.df.empty: return []
        high_lat_eps = self.df[self.df["Latency"] > threshold]["EndpointID"].unique().tolist()
        return sorted(high_lat_eps)
    
    def count_high_latency_endpoints(self, threshold: int) -> int:
        """Count unique endpoints with latency above threshold."""
        return len(self.high_latency_endpoints(threshold))
