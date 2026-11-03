"""
QP-212: Server Traffic Logs Analysis

A Python class for analyzing server traffic logs using pandas.
The class can load CSV data, clean outliers, handle missing values,
and provide traffic statistics.
"""

import pandas as pd


class TrafficAnalyzer:
    """Analyzes server traffic logs for performance metrics and error tracking."""
    
    def __init__(self):
        """Initialize the TrafficAnalyzer with an empty DataFrame."""
        self.df = None
    
    def read_logs(self, file_path: str):
        """
        Load CSV traffic logs into the DataFrame.
        
        Args:
            file_path (str): Path to the CSV file containing traffic logs
        """
        self.df = pd.read_csv(file_path)
    
    def sanitize_latency(self) -> int:
        """
        Identify and remove outliers (ResponseTime > 10.0 seconds).
        
        Returns:
            int: Number of outlier rows removed
        """
        if self.df is None:
            return 0
        
        outlier_count = len(self.df[self.df['ResponseTime'] > 10.0])
        # Keep rows where ResponseTime <= 10.0 OR ResponseTime is NaN
        self.df = self.df[(self.df['ResponseTime'] <= 10.0) | (self.df['ResponseTime'].isna())].copy()
        return outlier_count
    
    def fix_missing_records(self):
        """
        Fill NaN values in ResponseTime column with the mean of existing values.
        """
        if self.df is None:
            return
        
        mean_response_time = self.df['ResponseTime'].mean()
        self.df['ResponseTime'] = self.df['ResponseTime'].fillna(mean_response_time)
    
    def get_slowest_endpoint(self) -> str:
        """
        Identify the endpoint with the highest average response time.
        
        Returns:
            str: The endpoint path with the slowest average response time
        """
        if self.df is None or len(self.df) == 0:
            return ""
        
        slowest = self.df.groupby('Endpoint')['ResponseTime'].mean().idxmax()
        return slowest
    
    def count_errors(self, error_code: int) -> int:
        """
        Count the number of errors with a specific HTTP status code.
        
        Args:
            error_code (int): HTTP error code to count (e.g., 404, 500)
        
        Returns:
            int: Number of occurrences of the error code
        """
        if self.df is None:
            return 0
        
        count = len(self.df[self.df['StatusCode'] == error_code])
        return count
