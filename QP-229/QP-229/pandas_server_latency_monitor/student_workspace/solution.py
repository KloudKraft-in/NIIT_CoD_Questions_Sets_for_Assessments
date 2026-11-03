import pandas as pd
import numpy as np

class ServerLatencyMonitor:
    """Server Latency Monitoring System using Pandas."""
    
    def __init__(self):
        """Initialize the ServerLatencyMonitor with an empty DataFrame."""
        self.df = None
    
    def read_data(self, file_path: str):
        """Load the CSV file into a Pandas DataFrame."""
        self.df = pd.read_csv(file_path)
    
    def clean_records(self) -> int:
        """Drop NaN rows in 'Latency' and return count of dropped rows."""
        pass
    
    def find_highest_latency(self) -> int:
        """Return maximum latency."""
        pass
    
    def endpoint_averages(self) -> dict:
        """Return dict of {EndpointID: mean_latency} rounded to 2 decimal places."""
        pass
    
    def high_latency_endpoints(self, threshold: int) -> list:
        """Return sorted list of unique EndpointIDs above threshold."""
        pass
    
    def count_high_latency_endpoints(self, threshold: int) -> int:
        """Return count of high-latency endpoints."""
        pass
