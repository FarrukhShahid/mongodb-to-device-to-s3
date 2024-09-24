import argparse
import os
from dotenv import load_dotenv
from backup_mongodb import backup_mongodb
from upload_to_s3 import upload_to_s3

# Load environment variables from .env file
load_dotenv()

def main():
    # Argument parser for taking inputs
    parser = argparse.ArgumentParser(description='MongoDB Backup and Upload to S3')

    # Parameters for backup
    parser.add_argument('--mongo-uri', type=str, default=os.getenv('MONGO_URI'),
                        help='MongoDB connection URI (default taken from .env)')
    parser.add_argument('--db-name', type=str, default=os.getenv('DB_NAME'),
                        help='Name of the MongoDB database to backup (default taken from .env)')
    parser.add_argument('--output-dir', type=str, default=os.getenv('OUTPUT_DIR', 'mongodb_backup'),
                        help='Directory to store the backup (default taken from .env or "mongodb_backup")')

    # Parameters for S3 upload
    parser.add_argument('--aws-access-key', type=str, default=os.getenv('AWS_ACCESS_KEY'),
                        help='Your AWS Access Key (default taken from .env)')
    parser.add_argument('--aws-secret-key', type=str, default=os.getenv('AWS_SECRET_KEY'),
                        help='Your AWS Secret Key (default taken from .env)')
    parser.add_argument('--s3-bucket', type=str, default=os.getenv('S3_BUCKET'),
                        help='Name of the S3 bucket to upload the backup to (default taken from .env)')

    # Option to only backup, only upload, or both
    parser.add_argument('--action', choices=['backup', 'upload', 'both'], default='both',
                        help="Choose to either 'backup', 'upload' or 'both' (default: both)")

    args = parser.parse_args()

    # Error checking for upload parameters
    if args.action in ['upload', 'both'] and (not args.aws_access_key or not args.aws_secret_key or not args.s3_bucket):
        print("Error: For upload or both actions, --aws-access-key, --aws-secret-key, and --s3-bucket are required.")
        parser.print_help()
        return

    # Perform backup
    if args.action in ['backup', 'both']:
        print("Starting MongoDB Backup...")
        backup_mongodb(args.mongo_uri, args.db_name, args.output_dir)

    # Perform upload to S3
    if args.action in ['upload', 'both']:
        print("Uploading backup to S3...")
        upload_to_s3(args.aws_access_key, args.aws_secret_key, args.s3_bucket, args.output_dir)

if __name__ == "__main__":
    main()
