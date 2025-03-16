from pyspark.sql import Window
from pyspark.sql.functions import (
    col, sum, avg, lag, dense_rank, desc, when, max, min, count, concat_ws, lit
)
from resources.dev import config
from src.main.utility.logging_config import logger
from src.main.write.database_write import DatabaseWriter

def sales_mart_calculation_table_write(sales_team_mart_df):
    # Add the `full_name` column
    sales_team_mart_df = (sales_team_mart_df.withColumn(
        "full_name", concat_ws(" ", col("sales_person_first_name"), col("sales_person_last_name"))
    ))

    # Total sales for each salesperson per store and month
    window1 = Window.partitionBy('sales_month', 'store_id', 'sales_person_id')
    sales_team_mart_df = sales_team_mart_df.withColumn('total_sales', sum('total_cost').over(window1))

    # Average Sales Per Month
    avg_sales_window = Window.partitionBy('sales_person_id')
    sales_team_mart_df = sales_team_mart_df.withColumn('avg_sales_per_month', avg('total_sales').over(avg_sales_window))


    # Rank Salespeople within each store & incentive
    window2 = Window.partitionBy('sales_month', 'store_id').orderBy(desc('total_sales'))
    sales_team_mart_df = sales_team_mart_df.withColumn('top_performance_rank', dense_rank().over(window2))

    # Calculate Incentives for Top Performers
    sales_team_mart_df = sales_team_mart_df.withColumn(
        'incentive', when(col('top_performance_rank') == 1, col('total_sales') * 0.01).otherwise(lit(0))
    )

    # Sales Growth Rate (Month-over-Month)
    growth_window = Window.partitionBy('store_id').orderBy('sales_month')
    sales_team_mart_df = sales_team_mart_df.withColumn('previous_month_sales', lag('total_sales').over(growth_window)) \
        .withColumn(
            'sales_growth_rate',
            when(col('previous_month_sales').isNotNull(),
                 ((col('total_sales') - col('previous_month_sales')) / col('previous_month_sales')) * 100
            ).otherwise(None)
        )

    # Year-to-Date Sales with data validation
    max_value = lit(2147483647)  # For INT type in MySQL
    year_window = Window.partitionBy('store_id', col('sales_month').substr(1, 4))
    sales_team_mart_df = sales_team_mart_df.withColumn(
        'year_to_date_sales', sum('total_sales').over(year_window)
    ).withColumn(
        'year_to_date_sales',
        when(col('year_to_date_sales') <= max_value, col('year_to_date_sales')).otherwise(None)
    )

    # Month-over-Month Variance
    sales_team_mart_df = sales_team_mart_df.withColumn(
        'month_over_month_variance',
        when(col('previous_month_sales').isNotNull(),
             col('total_sales') - col('previous_month_sales')
        ).otherwise(None)
    )

    # First and Last Sale Month for Each Salesperson
    sales_time_window = Window.partitionBy('sales_person_id')
    sales_team_mart_df = sales_team_mart_df.withColumn(
        'first_sale_month', min('sales_month').over(sales_time_window)
    ).withColumn(
        'last_sale_month', max('sales_month').over(sales_time_window)
    )

    # Total Transactions for Each Salesperson
    sales_team_mart_df = sales_team_mart_df.withColumn(
        'total_transactions', count('sales_month').over(window1)
    )

    # Average Transaction Value
    sales_team_mart_df = sales_team_mart_df.withColumn(
        'avg_transaction_value',
        when(col('total_transactions') > 0, col('total_sales') / col('total_transactions')).otherwise(None)
    )

    # Maximum Single Sale Value
    sales_team_mart_df = sales_team_mart_df.withColumn(
        'max_single_transaction', max('total_cost').over(window1)
    )

    # Sales Contribution Percentage per Store
    store_total_sales_window = Window.partitionBy('store_id', 'sales_month')
    sales_team_mart_df = sales_team_mart_df.withColumn(
        'sales_contribution_percentage',
        (col('total_sales') / sum('total_sales').over(store_total_sales_window)) * 100
    )

    # Select final output columns
    sales_team_mart_df = sales_team_mart_df.select(
        'store_id', 'sales_person_id', 'full_name', 'sales_month',
        'total_sales', 'avg_sales_per_month', 'incentive', 'sales_growth_rate',
        'top_performance_rank', 'year_to_date_sales', 'month_over_month_variance',
        'first_sale_month', 'last_sale_month', 'total_transactions',
        'avg_transaction_value', 'max_single_transaction', 'sales_contribution_percentage'
    ).distinct()

    # Inspect and log problematic values
    sales_team_mart_df.select('store_id', 'sales_person_id', 'year_to_date_sales').show(truncate=False)

    # Write to database
    logger.info(f"{'*' * 20} Writing sales_team data mart to table {config.sales_team_data_mart_table} {'*' * 20}")
    try:
        db_writer = DatabaseWriter(url=config.url, properties=config.properties)
        db_writer.write_dataframe(sales_team_mart_df, config.sales_team_data_mart_table)
    except Exception as e:
        logger.error(f'{e}')
