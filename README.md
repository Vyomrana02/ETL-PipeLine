# ETL Data Engineering Project

## Overview
This project is a robust ETL (Extract, Transform, Load) pipeline designed to efficiently handle large-scale data processing for business analytics and decision-making. It focuses on integrating data from multiple sources, applying transformation logic, and generating valuable insights for business teams. The pipeline is tailored to ensure high data quality, reliability, and security.

---

## Key Features

### 1. **Scalable and Modular Architecture** (To be add)
   - The pipeline is designed with a modular approach, allowing new data sources, transformations, or destinations to be added with minimal changes.
   - Highly scalable to handle increasing data volumes.

### 2. **Data Quality and Validation**
   - Includes pre-defined validation checks to ensure accurate and consistent data at all stages.
   - Automatic alerts for missing or corrupt data for quick resolution. (To be add)

### 3. **Self-Healing Mechanism**(Add)
   - The system includes a self-healing mechanism to handle failures during processing:
     - Automatic retries for temporary network or processing failures.
   - Error notifications are sent to relevant stakeholders for quick action.

### 4. **Encryption and Security**
   - Secure storage and transfer of data using encryption protocols.
   - Credential management via a trusted provider to prevent unauthorized access.

### 5. **Business-Oriented Metrics**
   - Built-in calculations for KPIs (Key Performance Indicators) to monitor customer behavior and sales team performance.

---

## Business Goals
The ETL project aims to address the following business objectives:

1. **Customer Insights:**
   - Identify and segment high-value customers to personalize marketing campaigns.
   - Analyze trends in customer behavior to improve retention strategies.

2. **Sales Optimization:**
   - Provide actionable insights into sales team performance.
   - Track growth trends and rank top-performing salespersons.

3. **Operational Efficiency:**
   - Automate manual data processing to save time and reduce errors.
   - Improve decision-making processes by delivering reliable and timely data.

4. **Risk Mitigation:**
   - Detect anomalies in sales or customer data for fraud prevention.
   - Flag inactive customers to minimize loss from dormant accounts.

---

## Metrics Information for ETL Data Engineering Project

This document provides a detailed explanation of the metrics calculated for the **Customers Data Mart** and **Sales Team Data Mart** tables in the project. These metrics are essential for analyzing customer behavior, sales performance, and overall business insights.

---

### Metrics in Customers Data Mart

| Metric Name                 | Description                                                                                           |
|-----------------------------|-------------------------------------------------------------------------------------------------------|
| **customer_id**             | Unique identifier for each customer.                                                                |
| **full_name**               | Concatenation of the customer's first and last name.                                                |
| **address**                 | Complete address of the customer.                                                                   |
| **phone_number**            | Contact number of the customer.                                                                     |
| **sales_date_month**        | The month in which sales transactions occurred, in the format `YYYY-MM`.                           |
| **total_sales**             | Total sales amount made by the customer across all purchases.                                       |
| **customer_lifetime_value** | Total value of the customer to the business over their entire relationship.                         |
| **first_purchase_month**    | The month of the customer’s first recorded purchase, in the format `YYYY-MM`.                      |
| **last_purchase_month**     | The month of the customer’s most recent purchase, in the format `YYYY-MM`.                         |
| **purchase_frequency**      | Total number of purchases made by the customer.                                                    |
| **monetary_value**          | Average amount spent by the customer per transaction.                                              |
| **avg_monthly_spending**    | Average spending by the customer per month.                                                        |
| **max_single_transaction**  | The highest amount spent by the customer in a single transaction.                                  |
| **avg_time_between_purchases** | Average number of days between consecutive purchases made by the customer.                        |
| **inactive_status**         | A boolean value indicating whether the customer is inactive (`TRUE` = inactive).                   |
| **customer_segment**        | Classification of the customer based on their behavior or spending (e.g., Premium, Regular).        |

---

### Metrics in Sales Team Data Mart

| Metric Name                   | Description                                                                                           |
|-------------------------------|-------------------------------------------------------------------------------------------------------|
| **store_id**                  | Unique identifier for each store.                                                                    |
| **sales_person_id**           | Unique identifier for each salesperson.                                                              |
| **full_name**                 | Full name of the salesperson.                                                                        |
| **sales_month**               | Month in which the sales occurred, in the format `YYYY-MM`.                                          |
| **total_sales**               | Total sales made by the salesperson during the month.                                                |
| **avg_sales_per_month**       | Average monthly sales for the salesperson.                                                           |
| **incentive**                 | Monetary incentive earned by the salesperson based on their performance.                             |
| **sales_growth_rate**         | Growth rate of sales compared to the previous month, calculated as a percentage.                     |
| **top_performance_rank**      | Ranking of the salesperson in their store based on total sales.                                      |
| **year_to_date_sales**        | Cumulative sales made by the salesperson in the current year.                                        |
| **month_over_month_variance** | Difference in total sales compared to the previous month.                                            |
| **first_sale_month**          | The month of the salesperson’s first recorded sale, in the format `YYYY-MM`.                        |
| **last_sale_month**           | The month of the salesperson’s most recent sale, in the format `YYYY-MM`.                           |
| **total_transactions**        | Total number of sales transactions handled by the salesperson.                                       |
| **avg_transaction_value**     | Average value of each sales transaction handled by the salesperson.                                  |
| **max_single_transaction**    | The highest value of a single transaction handled by the salesperson.                                |
| **sales_contribution_percentage** | The percentage contribution of the salesperson’s sales to the store’s total sales.                |

---

## Usage
These metrics are calculated during the ETL process to provide actionable insights into customer and sales team performance. They can be used for:
- Identifying high-value customers and customer retention strategies.
- Evaluating salesperson performance and sales growth trends.
- Decision-making for business strategies and resource allocation.

---

## Prerequisites
Ensure the following tools and dependencies are installed:
- Python 3.x
- `pip` (Python package manager)
- Required Python packages (specified in `requirements.txt`)
- SQL database for running the provided scripts
- Credential provider for secure access

---

## Installation and Setup

1. **Navigate to resource directory & install Required Python Dependencies Execute the following command to install all necessary Python packages:**
   ```bash
   pip install -r resources/dev/requirements.txt

2. **Run SQL Scripts Locate the SQL script (table_scripts.sql) in the resources/sql_scripts directory and execute it in your SQL database. Path:
   ```bash
   resources/sql_scripts/table_scripts.sql
Use your database client or CLI to execute the script in mysqlserver.

3. **Generate and Process Data Files Execute the upload_files.py script to handle data file generation and upload:
    ```bash
   python src/test/generate_csv_data.py
   python src/test/generate_customer_table_data.py
   python upload_files.py

4. **Handle Encryption and Decryption (Optional) If encryption and decryption are required for AWS_SECRET_KEY & AWS_ACCESS_KEY, you can run the encrypt_decrypt.py script. However, if you’re utilizing a credential provider, this step is not needed.
    ```bash
   python src/main/utility/encrypt_decrypt.py 

Notes
- Modify configuration files or environment variables as necessary to suit your setup. 
- Ensure appropriate permissions are granted to access the database and credential provider. 
- Review the scripts before running to align with your data and schema requirements. 

Contact 
- If you encounter any issues or have questions, please feel free to reach out to the project maintainer.
