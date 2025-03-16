from resources.dev.config import generate_data_path
from src.main.utility.logging_config import logger
from src.main.utility.encrypt_decrypt import *
from boto3 import client

# Initialize S3 client
s3_client = client("s3")

local_file_path = generate_data_path

def upload_to_s3(s3_directory, s3_bucket, local_file_path):
    s3_prefix = f"{s3_directory}"
    print(s3_prefix)
    try:
        for root, dirs, files in os.walk(local_file_path):
            for file in files:
                print(file)
                local_file_path = os.path.join(root, file)
                s3_key = f"{s3_prefix}{file}"
                s3_client.upload_file(local_file_path, s3_bucket, s3_key)
            print("SUCCESS")
    except Exception as e:
        raise e

def delete_local_files(directory_path):
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)  # Delete the file
                print(f"Deleted file: {file_path}")
        logger.info("All files deleted successfully from the directory.")
    except Exception as e:
        logger.error(f"Error while deleting files: {e}")
        raise e

s3_directory = config.s3_source_directory
s3_bucket = config.bucket_name

upload_to_s3(s3_directory, s3_bucket, local_file_path)

logger.info("File uploaded successfully")

delete_local_files(local_file_path)
