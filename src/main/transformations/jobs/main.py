# from resources.dev.config import aws_access_key, aws_secret_key
# #from src.main.utility.encrypt_decrypt import decrypt
# from src.main.utility.logging_config import logger
# from  src.main.utility.s3_client_object import S3ClientProvider
#
# when not able to find the access key and secret key from credentialprovider
# s3_client_provider = S3ClientProvider("ACCESSKEY","SECRETKEY")
# s3_client = s3_client_provider.get_client()
#
# response = s3_client.list_buckets()
# print(response)


import sys

from resources.dev.config import *
from src.main.delete.local_file_delete import delete_local_file
from src.main.download.aws_file_download import S3FileDownloader
from src.main.move.move_files import move_s3_to_s3
from src.main.read.database_read import DatabaseReader
from src.main.transformations.jobs.customer_mart_sql_tranform_write import customer_mart_calculation_table_write
from src.main.transformations.jobs.dimension_tables_join import dimesions_table_join
from src.main.transformations.jobs.sales_mart_sql_transform_write import sales_mart_calculation_table_write
from src.main.upload.upload_to_s3 import UploadToS3

from boto3 import client
from src.main.utility.my_sql_session import *
import os
from src.main.read.aws_read import *
from src.main.utility.spark_session import *
import datetime
from pyspark.sql.functions import *
from pyspark.sql.types import *
from src.main.write.parquet_writer import ParquetWriter

# ---------------------------------------------------------------------------------------------------------
#s3_client_provider = S3ClientProvider(decrypt(aws_access_key) , decrypt(aws_secret_key))
s3_client = client("s3")
bucket_info = s3_client.list_buckets()

logger.info('List of buckets = {}'.format(bucket_info['Buckets']))

#----------------------------------------------------------------------------------------------------------
files_locally = [files for files in os.listdir(local_directory) if files.endswith('csv')]
db_connc = get_mysql_connection()
cursor = db_connc.cursor()

#get unprocssed files from DB
if files_locally:
    query = f'''
         select file_name , status from {database_name}.product_staging_table where file_name in
         ({str(files_locally)[1:-1]}) and status = 'A'
        '''
    logger.info(f'Query executed : {query}')
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        unprocessed_files = [row[0] for row in rows]
        logger.info('process failed for these files : {}'.format(unprocessed_files))
    else:
        logger.info('All the file successfully processed')
else:
    logger.info('Files processed and removed from local')

#-------------------------------------------------------------------------------------------------------------
# read data from s3
try:
    files_lst = S3Reader().list_files(s3_client , bucket_name , s3_source_directory)
    if files_lst:
      logger.info(f'Files to be read : {files_lst}')
    else:
        raise Exception(f's3 bucket empty')
except Exception as e:
    logger.error(f'Exception raised : {e}')

#download data from s3 to local
try:
    s3_downloader = S3FileDownloader(s3_client , bucket_name , local_directory)
    s3_downloader.download_files(files_lst)
except Exception as e:
    logger.error(f'Error while downloading files from s3 : {e}')


all_files = os.listdir(local_directory)
logger.info(f'List of files locally : {all_files}')

# take only csv files for processing
csv_files = []
other_files = []
local_files_lst = os.listdir(local_directory)
for file in local_files_lst:
    if file.endswith('csv'):
        csv_files.append(os.path.join(local_directory , file))
    else:
        other_files.append(os.path.join(local_directory , file))

try:
    if csv_files:
        logger.info(f'list of files for processing : {csv_files}' )
    else:
        raise Exception('No csv files for processing')
except Exception as e:
    logger.error(e)

#----------------------------------------------------------------------------------------------------------

logger.info(f"{'*'*20} Spark session created{'*'*20}")
spark = spark_session()

# take only that csv files which are having valid schema
logger.info(f"{'*'*20} Schema validation {'*'*20}")
for file in csv_files:
    file_columns = spark.read \
              .format('csv') \
              .option('header' , True) \
              .load(file) \
              .columns
    logger.info(f'list of columns for {file} is : {file_columns}')
    logger.info(f'mandatory columns : {mandatory_columns}')
    missing_cols = set(mandatory_columns) - set(file_columns)
    logger.info(f'missing columns are : {list(missing_cols)}')
    if missing_cols:
        other_files.append(file)
        csv_files.remove(file)

logger.info(f'final csv files for processing {set(csv_files) - set(other_files)}')
logger.info(f'error files : {other_files}')
logger.info(f"{'*'*20} moving the files to error directory {'*'*20}")


# move error files - either not csv or not as per the schema
try:
    if other_files:
        for file in other_files:
            if os.path.exists(file):
                file_name = os.path.basename(file)
                dst = os.path.join(error_folder_path_local , file_name)
                os.rename(file , dst)
                msg = move_s3_to_s3(s3_client , bucket_name , s3_source_directory , s3_error_directory , file_name)
                logger.info(msg)
            else:
                raise Exception(f'file {file} does not exists')
        logger.info(f'files moved to error folder : {os.listdir(error_folder_path_local)}')
    else:
        logger.info(f'no error files to move')

except Exception as e:
    logger.error(f'Error in moving files : {e}')

#----------------------------------------------------------------------------------------------------------
#insert the csv files metadata in the sales.product_staging_table

logger.info(f"{'*'*20} inserting in staging table {'*'*20}")

connc = get_mysql_connection()
cursor = connc.cursor()
currdt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for file in csv_files:
    file_name = os.path.basename(file)
    query = f'''
      insert into {database_name}.{product_staging_table}(file_name , file_location , created_date  , status)
      values ('{file_name}' , '{file_name}' , '{currdt}' , 'A')
    '''
    logger.info(f'Query executed : {query}')

    cursor.execute(query)
    connc.commit()

cursor.close()
connc.close()

logger.info(f"{'*'*30} creating data to be processed {'*'*30}")

final_sch = StructType([
    StructField('customer_id' , IntegerType()),
    StructField('store_id' , IntegerType()),
    StructField('product_name' , StringType()),
    StructField('sales_date' , DateType()),
    StructField('sales_person_id' , IntegerType()),
    StructField('price' , FloatType()),
    StructField('quantity' , IntegerType()),
    StructField('total_cost' , FloatType()),
    StructField('additional_columns' , StringType() , True)
])


# creating an empty dataframe for union
logger.info(f"{'*'*20} creating empty dataframe {'*'*20}")
final_df = spark.createDataFrame(data = [(None , )*9] , schema = final_sch)
final_df = final_df.where(col('customer_id').isNotNull())
#final_df = DatabaseReader(url , properties).create_dataframe(spark,'tab_structure')
final_df.show()

print(csv_files)
#inserting all the data to be processed in final_df
for file in csv_files:
    print(file)
    df = spark.read \
              .format('csv') \
              .option('header' , True) \
              .option('inferSchema' , True) \
              .load(file)

    # Remove duplicate rows from the DataFrame
    df = df.dropDuplicates()
    logger.info("Removed duplicate rows.")

    # Filter out rows with negative or invalid numeric values
    df_valid_numeric = df.filter((col('price') >= 0) & (col('quantity') >= 0) & (col('total_cost') >= 0))
    logger.info("Filtered out rows with invalid numeric values.")

    # Separate valid and invalid rows based on missing mandatory fields
    valid_rows = df_valid_numeric.filter(
        col('customer_id').isNotNull() &
        col('store_id').isNotNull() &
        col('product_name').isNotNull() &
        col('sales_date').isNotNull() &
        col('sales_person_id').isNotNull()
    )

    invalid_rows = df.subtract(valid_rows)

    # Log invalid rows and move them to an error directory
    invalid_rows.write.format('csv').mode('append').save(error_folder_path_local)
    logger.info(f"Moved invalid rows to error directory: {error_folder_path_local}")

    # Calculate total_cost and filter inconsistent rows
    valid_rows_with_cost_calculation = valid_rows.withColumn('calculated_total_cost', col('price') * col('quantity'))

    # Identify rows with mismatched total_cost
    inconsistent_rows = valid_rows_with_cost_calculation.filter(col('total_cost') != col('calculated_total_cost'))

    # Log mismatched rows and isolate them for further analysis
    inconsistent_rows.write.format('csv').mode('append').save(error_folder_path_local)
    logger.info(f"Moved inconsistent rows to error directory: {error_folder_path_local}")

    # Keep only consistent rows
    valid_df = valid_rows_with_cost_calculation.filter(col('total_cost') == col('calculated_total_cost'))

    df_cols = valid_df.columns
    extra_cols = set(df_cols) - set(mandatory_columns)
    print(df_cols)
    print(mandatory_columns)
    logger.info("Extra Columns present at source are: %s",extra_cols)
    if extra_cols:
        # all extra cols other then mandatory cols are added in additional_columns ie col name = additional_columns and row value = 50,North,SAVE10
        valid_df = valid_df.withColumn('additional_columns' , concat_ws(',' , *extra_cols))\
        .select("customer_id","store_id","product_name","sales_date","sales_person_id","price","quantity","total_cost","additional_columns")
        logger.info(f"Processed {file} and added 'additional_columns")
    else:
        valid_df = valid_df.withColumn('additional_columns' , lit(None)) \
        .select("customer_id", "store_id", "product_name", "sales_date", "sales_person_id", "price", "quantity",
                    "total_cost", "additional_columns")

    valid_df = valid_df.select(*mandatory_columns , 'additional_columns')
    final_df = final_df.union(valid_df)
logger.info(f"{'*'*20} final data to be processed {'*'*20}")
final_df.show()

#--------------------------------------------------------------------------------------------------------------

db_reader = DatabaseReader(url , properties)

logger.info(f"{'*'*20} creating {customer_table_name} table {'*'*20}")
customer_df = db_reader.create_dataframe(spark,customer_table_name)

logger.info(f"{'*'*20} creating {store_table} table {'*'*20}")
store_df = db_reader.create_dataframe(spark,store_table)

logger.info(f"{'*'*20} creating {sales_team_table} table {'*'*20}")
sales_team_df = db_reader.create_dataframe(spark,sales_team_table)

logger.info(f"{'*'*20} creating {product_table} table {'*'*20}")
product_df = db_reader.create_dataframe(spark,product_table)

logger.info(f"{'*'*20} creating {product_staging_table} table {'*'*20}")
product_staging_df = db_reader.create_dataframe(spark,product_staging_table)



tables_join_df = dimesions_table_join(final_df,customer_df,store_df,sales_team_df)
logger.info(f"{'*'*20} final enriched data {'*'*20}")
tables_join_df.show()

#only customer side of tables_join_df
cutsomer_mart_df = tables_join_df.select('ct.customer_id' , 'ct.first_name' , 'ct.last_name' ,
                                         'ct.address' , 'ct.phone_number' ,'sales_date' , 'total_cost')
logger.info(f"{'*'*20} customer data mart {'*'*20}")
cutsomer_mart_df.show(truncate = False)

try:
    logger.info(f"{'*'*20} writing customer data to local {'*'*20}")
    writer = ParquetWriter(mode = 'overwrite' , data_format = 'parquet')
    writer.dataframe_writer(cutsomer_mart_df , customer_data_mart_local_file)

except Exception as e:
    logger.error(f'error while writing to customer data mart : {e}')
    sys.exit(0)


try:
    logger.info(f"{'*'*20} moving customer data from local to s3 directory {s3_customer_datamart_directory} {'*'*20}")
    upload_s3 = UploadToS3(s3_client)
    upload_msg = upload_s3.upload_to_s3(s3_customer_datamart_directory,bucket_name,customer_data_mart_local_file)
    logger.info(upload_msg)

except Exception as e:
    logger.error(e)


# --------------------------------------------------------------------------------------------------------------
#only sales side data from tables_join_df

sales_team_mart_df = tables_join_df.select('store_id' ,
                                           'sales_person_id' ,
                                           'sales_person_first_name' ,
                                           'sales_person_last_name' ,
                                           concat_ws('-', year('sales_date'), month('sales_date')).alias('sales_month') ,
                                           'total_cost'
                                           )
logger.info(f"{'*'*20} sales team data mart {'*'*20}")
sales_team_mart_df.show(truncate = False)

try:
    logger.info(f"{'*'*20} writing sales team data to local {'*'*20}")
    writer = ParquetWriter(mode = 'overwrite' , data_format = 'parquet')
    writer.dataframe_writer(sales_team_mart_df , sales_team_data_mart_local_file)

except Exception as e:
    logger.error(f'error while writing to sales team data mart : {e}')
    sys.exit(0)


try:
    logger.info(f"{'*'*20} moving sales team data from local to s3 directory {sales_team_data_mart_local_file} {'*'*20}")
    upload_s3 = UploadToS3(s3_client)
    upload_msg = upload_s3.upload_to_s3(s3_sales_datamart_directory,bucket_name,sales_team_data_mart_local_file)
    logger.info(upload_msg)

except Exception as e:
    logger.error(e)

#------------------------------------------------------------------------------------------------------------
#partioned sales data mart on month

logger.info(f"{'*'*20} creating partitioned data for the sales team {'*'*20}")

sales_team_mart_df.write \
                  .format('parquet') \
                  .mode('overwrite') \
                  .partitionBy('sales_month' , 'store_id') \
                  .save(sales_team_data_mart_partitioned_local_file)

logger.info(f"{'*'*20} moving sales team partitioned data from local to s3 {'*'*20}")
s3_prefix = 'sales_partitioned_data_mart/'
current_epoch = int(datetime.datetime.now().timestamp()) * 1000
s3_path = f'{s3_prefix}/{current_epoch}'
try:
    for root , dirs , files in os.walk(sales_team_data_mart_partitioned_local_file):
        for file in files:
            abs_path_file = os.path.join(root,file)
            rel_path = abs_path_file[len(sales_team_data_mart_partitioned_local_file):]
            s3_key = f'{s3_path}/{rel_path}'
            s3_client.upload_file(abs_path_file , bucket_name , s3_key)
            print(file)
except Exception as e:
    logger.error(f'failed to upload to s3 : {e}')

#-------------------------------------------------------------------------------------------------------

logger.info(f"{'*'*20} writing customer data to table {customer_table_name} {'*'*20}")
customer_mart_calculation_table_write(cutsomer_mart_df)

logger.info(f"{'*' * 20} preparing sales_team_data_mart table {'*' * 20}")
sales_mart_calculation_table_write(sales_team_mart_df)
#-------------------------------------------------------------------------------------------------------

logger.info(f"{'*'*20} deleting files from the local directories {'*'*20}")

try:
    delete_local_file(local_directory)
    delete_local_file(customer_data_mart_local_file)
    delete_local_file(sales_team_data_mart_local_file)
    delete_local_file(sales_team_data_mart_partitioned_local_file)
    delete_local_file(error_folder_path_local)
except Exception as e:
    logger.error(f'{e}')



logger.info(f"{'*'*20} updating sql table {product_staging_table} for active processes {'*'*20}")
db_connc = get_mysql_connection()
cursor = db_connc.cursor()

for file in csv_files:
    query = f'''
    update {database_name}.{product_staging_table} 
    set updated_date = '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',
    status = 'I' where file_name = '{os.path.basename(file)}'
    '''
    cursor.execute(query)
    db_connc.commit()

cursor.close()
db_connc.close()


a = input('press to terminate')
