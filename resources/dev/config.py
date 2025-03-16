import os

key = "this_is_a_16byte_"  # 16 bytes (exact length required for AES-128)
iv = "16byte_iv_value!"    # 16 bytes (exactly required for CBC mode)
salt = "salt_value_for_pbkdf"  # Arbitrary length (but consistent between encryption and decryption)


#AWS Access And Secret key
aws_access_key = "<YOUR_ACCESS_KEY>"
aws_secret_key = "<YOUR_SECRET_KEY>"
bucket_name = "<BUCKET_NAME>"
base_path_after_bucket = "<YOUR_BASE_PATH_AWS>"
s3_customer_datamart_directory = base_path_after_bucket +  "customer_data_mart"
s3_sales_datamart_directory = base_path_after_bucket + "sales_data_mart"
s3_source_directory = base_path_after_bucket + "sales_data/"
s3_error_directory = base_path_after_bucket + "sales_data_error/"
s3_processed_directory = base_path_after_bucket + "sales_data_processed/"


#Database credential
# MySQL database connection properties
database_name = "sales"
url = f"jdbc:mysql://localhost:3306/{database_name}"
properties = {
    "user": "root",
    "password": "rootuser",
    "driver": "com.mysql.cj.jdbc.Driver"
}

# Database
database_name = "sales"

# Table name
customer_table_name = "customer"
product_staging_table = "product_staging_table"
product_table = "product"
sales_team_table = "sales_team"
store_table = "store"

#Data Mart details
customer_data_mart_table = "customers_data_mart"
sales_team_data_mart_table = "sales_team_data_mart"

# Required columns
mandatory_columns = ["customer_id","store_id","product_name","sales_date","sales_person_id","price","quantity","total_cost"]


# File Download location
base_path = "<YOUR_BASE_PATH_LOCAL>"
local_directory = base_path + "file_from_s3/"
generate_data_path =  base_path + "generated_data/"
customer_data_mart_local_file =  base_path + "customer_data_mart"
sales_team_data_mart_local_file =  base_path + "sales_team_data_mart/"
sales_team_data_mart_partitioned_local_file =  base_path + "sales_partition_data/"
error_folder_path_local = base_path + "error_files/"