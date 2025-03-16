from pyspark.sql import Window
from pyspark.sql.functions import (
    col, sum, max, min, count, lit, substring, avg, datediff, current_date, when, concat, lag, months_between
)
from resources.dev import config
from src.main.write.database_write import DatabaseWriter
from src.main.utility.logging_config import logger

def customer_mart_calculation_table_write(final_customer_data_mart_df):
    # Add sales_date_month field for grouping
    window_monthly = Window.partitionBy("customer_id", "sales_date_month")
    final_customer_data_mart = final_customer_data_mart_df.withColumn(
        "sales_date_month", substring(col("sales_date"), 1, 7)  # Extract 'YYYY-MM'
    ).withColumn(
        "total_sales_every_month_by_each_customer", sum("total_cost").over(window_monthly)
    ).select(
        "customer_id",
        concat(col("first_name"), lit(" "), col("last_name")).alias("full_name"),
        "address", "phone_number", "sales_date_month",
        col("total_sales_every_month_by_each_customer").alias("total_sales")
    ).distinct()

    # Calculate Customer Lifetime Value (CLV)
    window_clv = Window.partitionBy("customer_id")
    final_customer_data_mart = final_customer_data_mart.withColumn(
        "customer_lifetime_value", sum("total_sales").over(window_clv)
    )

    # Define Purchase Frequency and Monetary Value
    rfm_window = Window.partitionBy("customer_id")
    final_customer_data_mart = final_customer_data_mart.withColumn(
        "last_purchase_month", max("sales_date_month").over(rfm_window)
    ).withColumn(
        "first_purchase_month", min("sales_date_month").over(rfm_window)
    ).withColumn(
        "purchase_frequency", count("sales_date_month").over(rfm_window)
    ).withColumn(
        "monetary_value", col("customer_lifetime_value") / col("purchase_frequency")  # Average transaction value of whole history
    )

    # Average Monthly Spending (ie avg purchase monthly)
    final_customer_data_mart = final_customer_data_mart.withColumn(
        "avg_monthly_spending", avg("total_sales").over(rfm_window)
    )

    # Max Single Transaction Value
    final_customer_data_mart = final_customer_data_mart.withColumn(
        "max_single_transaction", max("total_sales").over(Window.partitionBy("customer_id"))
    )

    # Average Time Between Purchases (in months)
    purchase_date_window = Window.partitionBy("customer_id").orderBy("sales_date_month")
    final_customer_data_mart = final_customer_data_mart.withColumn(
        "previous_purchase_date",
        lag("sales_date_month", 1).over(purchase_date_window)  # Get the previous purchase month
    ).withColumn(
        "time_between_purchases",
        months_between(col("sales_date_month"), col("previous_purchase_date"))  # Difference in months
    ).withColumn(
        "avg_time_between_purchases",
        avg("time_between_purchases").over(Window.partitionBy("customer_id"))  # Average time in months
    )

    # Determine Inactive Customers
    final_customer_data_mart = final_customer_data_mart.withColumn(
        "inactive_status", when(
            datediff(current_date(), concat(col("last_purchase_month"), lit("-01"))) > 180, True
        ).otherwise(False)
    )

    # Customer Segmentation Category
    final_customer_data_mart = final_customer_data_mart.withColumn(
        "customer_segment",
        when(col("purchase_frequency") >= 10, lit("Loyal Customer"))
        .when(col("monetary_value") >= 50000, lit("High-Value Customer"))
        .when(col("inactive_status") == True, lit("At-Risk Customer"))
        .otherwise(lit("Occasional Customer"))
    )

    # Select final output columns
    final_customer_data_mart = final_customer_data_mart.select(
        "customer_id", "full_name", "address", "phone_number", "sales_date_month",
        "total_sales", "customer_lifetime_value", "first_purchase_month", "last_purchase_month",
        "purchase_frequency", "monetary_value", "avg_monthly_spending", "max_single_transaction",
        "avg_time_between_purchases", "inactive_status", "customer_segment"
    ).distinct()

    # Write to database
    final_customer_data_mart.show(truncate=False)
    logger.info(f"{'*' * 20} Writing customer data mart to table {config.customer_data_mart_table} {'*' * 20}")
    try:
        db_writer = DatabaseWriter(url=config.url, properties=config.properties)
        db_writer.write_dataframe(final_customer_data_mart, config.customer_data_mart_table)
    except Exception as e:
        logger.error(f'{e}')
