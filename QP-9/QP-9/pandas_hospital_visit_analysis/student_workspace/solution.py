import pandas as pd

class HospitalAnalysis:

    def load_patients(self, file_path: str) -> pd.DataFrame:
        """Loads patient data from CSV"""
        return pd.read_csv(file_path)

    def load_visits(self, file_path: str) -> pd.DataFrame:
        """Loads visit data from CSV"""
        return pd.read_csv(file_path)

    def merge_dataframes(self, patients_df: pd.DataFrame, visits_df: pd.DataFrame) -> pd.DataFrame:
        """Merges patient and visit data on patient_id"""
        return pd.merge(patients_df, visits_df, on="patient_id", how="inner")

    def patient_with_most_visits(self, merged_df: pd.DataFrame) -> tuple:
        """
        Finds the patient with the most number of visits.
        Returns a tuple: (patient_name, visit_count)
        """
        visit_counts = merged_df.groupby("patient_name")["visit_id"].count()
        top_patient = visit_counts.sort_values(ascending=False).head(1)
        return (top_patient.index[0], int(top_patient.values[0]))

    def longest_visit_id(self, visits_df: pd.DataFrame) -> int:
        return int(visits_df.sort_values("duration", ascending=False).iloc[0]["visit_id"])

    def patients_with_no_visits(self, patients_df: pd.DataFrame, visits_df: pd.DataFrame) -> list:
        merged = pd.merge(patients_df, visits_df, on="patient_id", how="left", indicator=True)
        if "patient_name" not in merged.columns:
            raise ValueError("Column 'patient_name' missing after merge")
        return merged[merged["_merge"] == "left_only"]["patient_name"].tolist()

    def average_visit_duration(self, visits_df: pd.DataFrame) -> float:
        """Returns average visit duration"""
        return float(visits_df["duration"].mean())
