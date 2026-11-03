import pandas as pd

class SensorReading:
    def __init__(self, timestamp: str, value: float, sensor_id: str):
        # TODO: Initialize attributes
        pass

class TrendAnalyzer:
    def __init__(self):
        # TODO: Initialize self.df as None
        pass

    def load_data(self, csv_path: str):
        # TODO: Load CSV into self.df using pandas
        pass

    def convert_to_datetime(self):
        # TODO: Convert the 'Timestamp' column to datetime objects
        pass

    def filter_business_hours(self):
        # TODO: Keep only rows between 09:00:00 and 17:00:00 (inclusive)
        pass

    def calculate_hourly_means(self) -> pd.DataFrame:
        # TODO: Set Timestamp index and resample to '1H' mean
        # Return resulting DataFrame
        pass

    def get_heat_alerts(self, threshold: float) -> int:
        # TODO: Return count of Hourly Resampled Mean Values > threshold
        pass

    def get_max_reading_id(self) -> str:
        # TODO: Return the Sensor_ID associated with the single highest raw temperature
        pass