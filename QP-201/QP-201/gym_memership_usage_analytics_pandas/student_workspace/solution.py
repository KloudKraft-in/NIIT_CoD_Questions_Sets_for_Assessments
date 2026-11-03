import pandas as pd

class GymUsageAnalyzer:

    def create_usage_df(self, logs: list) -> pd.DataFrame:
        return pd.DataFrame(logs, columns=["Member", "Branch", "Workout", "Duration"])

    def compute_total_duration(self, usage_df: pd.DataFrame) -> pd.DataFrame:
        #your_code_here
        return result

    def add_calorie_column(self, usage_df: pd.DataFrame) -> pd.DataFrame:
        rates = {"Cardio": 8, "Weights": 7, "Yoga": 5}
        # Map workout type to burn rate; default to 6 if not found
         #your_code_here
        return df.drop(columns=["Rate"])

    def filter_long_sessions(self, usage_df: pd.DataFrame, min_minutes: int) -> pd.DataFrame:
        #your_code_here
        return 

    def get_top_sessions(self, usage_df: pd.DataFrame, n: int) -> pd.DataFrame:
        #your_code_here
        return top_session_df
    
    def remove_duplicates(self, usage_df: pd.DataFrame) -> pd.DataFrame:
        #your_code_here
        return unique_df

