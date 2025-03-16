import os
from pyspark.sql import SparkSession

def spark_session(app_name="MyApp"):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    mysql_connector_path = os.path.join(
        repo_root,
        "ETL-PipeLine-mysql-connector/mysql-connector-j-9.1.0.jar"
    )

    spark = SparkSession.builder \
        .appName("MyApp") \
        .config("spark.jars", mysql_connector_path) \
        .getOrCreate()

    return spark

if __name__ == "__main__":
    try:
        spark = spark_session("My Spark App")
        print("Spark session created successfully!")
    except Exception as e:
        print(f"Error creating Spark session: {e}")
