import pandas as pd
class HotelBookingAnalyzer:

    def create_booking_df(self, booking_data: list) -> pd.DataFrame:
        #your_code_here
        return df

    def compute_monthly_revenue(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # Filter only booked records
        booked_df = df[df["Status"] == "Booked"]
        
        # Extract month (YYYY-MM)
        booked_df = booked_df.copy()
        booked_df["Month"] = pd.to_datetime(booked_df["Date"]).dt.strftime("%Y-%m")
        
        # Group by Hotel and Month, sum Amount
        result = booked_df.groupby(["Hotel", "Month"])["Amount"].sum().reset_index()
        result.columns = ["Hotel", "Month", "Revenue"]
        return result

    def add_cancellation_flag(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a binary flag for cancelled bookings.
        Args:    df: Booking DataFrame
        Returns:    DataFrame with added IsCancelled column (1 or 0)
        """
        df = df.copy()
        df["IsCancelled"] = (df["Status"] == "Cancelled").astype(int)
        return df

    def get_no_show_guests(self, df: pd.DataFrame, threshold: int) -> pd.DataFrame:
        #your_code_here
        return result

    def hotel_status_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        status_counts = df.groupby(["Hotel", "Status"]).size()
        return result

    def clean_booking_data(self, df: pd.DataFrame) -> pd.DataFrame:
        #your_code_here
        return df

