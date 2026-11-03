from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, avg, desc, row_number
from pyspark.sql.window import Window

class ExamAnalyzer:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def load_data(self, students_path: str, scores_path: str) -> tuple[DataFrame, DataFrame]:
        """
        Load students and scores CSVs into Spark DataFrames.
        """
        students_df = self.spark.read.csv(students_path, header=True, inferSchema=True)
        scores_df = self.spark.read.csv(scores_path, header=True, inferSchema=True)
        return students_df, scores_df

    def join_data(self, students_df: DataFrame, scores_df: DataFrame) -> DataFrame:
        """
        Join students and scores on student_id.
        """
        return students_df.join(scores_df, on="student_id", how="inner")

    def top_scorer_per_subject(self, df: DataFrame) -> DataFrame:
        """
        For each subject, return the student with the highest score.
        """
        window_spec = Window.partitionBy("subject").orderBy(desc("score"))
        ranked_df = df.withColumn("rank", row_number().over(window_spec))
        return ranked_df.filter(col("rank") == 1).drop("rank")

    def average_score_by_class(self, df: DataFrame) -> DataFrame:
        """
        Return average score per class.
        """
        return df.groupBy("class").agg(avg("score").alias("average_score"))

    def students_missed_all_exams(self, students_df: DataFrame, scores_df: DataFrame) -> list[int]:
        """
        Return a list of student_ids who did not appear in scores.
        """
        left = students_df.join(scores_df, on="student_id", how="left")
        missed = left.filter(col("subject").isNull())
        return [int(row["student_id"]) for row in missed.select("student_id").collect()]

    def top_average_scorer(self, df: DataFrame) -> int:
        """
        Return the student_id with the highest average score across subjects.
        """
        avg_df = df.groupBy("student_id").agg(avg("score").alias("avg_score"))
        top = avg_df.orderBy(desc("avg_score")).first()
        return int(top["student_id"])
