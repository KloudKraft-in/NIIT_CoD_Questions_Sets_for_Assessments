from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, sum as _sum, desc


class SalesAnalyzer:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def load_transactions(self, sales_path: str) -> DataFrame:
        """
        Load transaction data from the sales CSV file into a Spark DataFrame.
        """
        return self.spark.read.csv(sales_path, header=True, inferSchema=True)

    def total_purchase_value(self, df: DataFrame) -> float:
        """
        Calculate the total value of all purchases (price * quantity).
        """
        df_with_total = df.withColumn("total_value", col("price") * col("quantity"))
        total = df_with_total.agg(_sum("total_value")).first()[0]
        return float(total)

    def top_product_category(self, df: DataFrame) -> tuple:
        """
        Identify the product category with the highest total sales (price * quantity).
        """
        df = df.withColumn("total_value", col("price") * col("quantity"))
        top_row = df.groupBy("category").agg(_sum("total_value").alias("total_sales")) \
                    .orderBy(desc("total_sales")) \
                    .first()
        return (top_row["category"], float(top_row["total_sales"]))

    def top_n_products(self, df: DataFrame) -> list:
        """
        Return a list of the top 3 product names by total quantity sold.
        """
        top_products = df.groupBy("product") \
                         .agg(_sum("quantity").alias("total_quantity")) \
                         .orderBy(desc("total_quantity")) \
                         .limit(3) \
                         .select("product") \
                         .rdd.flatMap(lambda row: row) \
                         .collect()
        return top_products
