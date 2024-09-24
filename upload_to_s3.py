import os
import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(aws_access_key, aws_secret_key, s3_bucket, backup_folder):
    # Initialize S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    # Upload each file in the backup folder
    if not os.path.exists(backup_folder):
        print(f"Error: Backup folder '{backup_folder}' does not exist.")
        return

    try:
        for root, dirs, files in os.walk(backup_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                s3_key = f"{backup_folder}/{file_name}"  # S3 object key
                
                try:
                    s3.upload_file(file_path, s3_bucket, s3_key)
                    print(f'Successfully uploaded {file_name} to {s3_bucket}/{s3_key}')
                except FileNotFoundError:
                    print(f'The file {file_path} was not found.')
                except NoCredentialsError:
                    print('Credentials not available.')
    except Exception as e:
        print(f"Error during upload: {str(e)}")
