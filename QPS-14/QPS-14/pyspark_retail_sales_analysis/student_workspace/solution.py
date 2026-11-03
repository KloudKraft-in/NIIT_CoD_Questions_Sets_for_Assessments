from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, expr, sum as spark_sum, desc

class RetailSalesAnalyzer:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def load_transactions(self, path: str) -> DataFrame:
        """
        Load the sales.csv file into a PySpark DataFrame.
        """
        return self.spark.read.csv(path, header=True, inferSchema=True)

    def total_purchase_value(self, df: DataFrame) -> float:
        """
        Compute total revenue by multiplying quantity and unit_price.
        """
        df_with_revenue = df.withColumn("revenue", col("quantity") * col("unit_price"))
        result = df_with_revenue.agg(spark_sum("revenue").alias("total")).first()
        return float(result["total"])

    def top_product_category(self, df: DataFrame) -> tuple:
        """
        Return the product category with the highest total revenue.
        """
        df_with_revenue = df.withColumn("revenue", col("quantity") * col("unit_price"))
        grouped = df_with_revenue.groupBy("product_category").agg(spark_sum("revenue").alias("total_revenue"))
        top = grouped.orderBy(desc("total_revenue")).first()
        return (top["product_category"], float(top["total_revenue"]))

    def top_n_products(self, df: DataFrame) -> list:
        """
        Return top 3 products based on quantity sold.
        """
        grouped = df.groupBy("product_name").agg(spark_sum("quantity").alias("total_quantity"))
        top3 = grouped.orderBy(desc("total_quantity")).limit(3).collect()
        return [(row["product_name"], row["total_quantity"]) for row in top3]
