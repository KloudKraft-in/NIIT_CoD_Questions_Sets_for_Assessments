# student_workspace/solution.py

import pandas as pd

class StudentPerformanceTracker:

    def load_student_data(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    def get_top_scorers(self, df: pd.DataFrame) -> pd.DataFrame:
        score_cols = df.columns.drop("name")
        mask = df[score_cols].gt(90).any(axis=1)
        return df[mask]

    def average_scores(self, df: pd.DataFrame) -> dict:
        score_cols = df.columns.drop("name")
        return df[score_cols].mean().round(2).to_dict()

    def top_students(self, df: pd.DataFrame) -> list:
        score_cols = df.columns.drop("name")
        df["total"] = df[score_cols].sum(axis=1)
        top3 = df.sort_values(by="total", ascending=False).head(3)
        return [(row["name"], int(row["total"])) for _, row in top3.iterrows()]
