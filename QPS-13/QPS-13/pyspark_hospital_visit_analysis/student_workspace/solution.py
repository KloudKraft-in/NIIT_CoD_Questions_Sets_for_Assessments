# student_workspace/solution.py

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import desc

class HospitalAnalyzer:
    def __init__(self, spark: SparkSession):
        """
        Initialize with an active SparkSession.
        """
        self.spark = spark

    def load_data(self, patients_path: str, visits_path: str) -> tuple[DataFrame, DataFrame]:
        """
        Load patients.csv and visits.csv into Spark DataFrames.
        """
        patients_df = self.spark.read.csv(patients_path, header=True, inferSchema=True)
        visits_df   = self.spark.read.csv(visits_path, header=True, inferSchema=True)
        return patients_df, visits_df

    def join_data(self, patients_df: DataFrame, visits_df: DataFrame) -> DataFrame:
        """
        Inner-join patients_df and visits_df on 'patient_id'.
        """
        return patients_df.join(visits_df, on="patient_id", how="inner")

    def most_frequent_visitor(self, df: DataFrame) -> int:
        row = df.groupBy("patient_id").count().orderBy(desc("count")).first()
        return int(row["patient_id"])  # Ensure pure Python int

        # Extract the patient_id field and cast to Python int
        return int(top_row["patient_id"])

    def longest_visit_id(self, df: DataFrame) -> int:
        """
        Return the visit_id of the visit with the longest duration.
        """
        top_row = df.orderBy(desc("duration")).first()
        return int(top_row["visit_id"])

    def patients_with_no_visits(self, patients_df: DataFrame, visits_df: DataFrame) -> list[int]:
        """
        Return a list of patient_ids that do not appear in visits_df.
        """
        left = patients_df.join(visits_df, on="patient_id", how="left")
        no_visits_df = left.filter(left["visit_id"].isNull())
        return [int(row["patient_id"]) for row in no_visits_df.select("patient_id").collect()]

    def average_visit_duration(self, visits_df: DataFrame) -> float:
        """
        Compute and return the average of the 'duration' column.
        """
        avg_row = visits_df.agg({"duration": "avg"}).first()
        return float(avg_row[0])
