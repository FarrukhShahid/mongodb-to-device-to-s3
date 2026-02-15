# mongodb-backup-s3

A Python package for backing up MongoDB databases to local storage and uploading backups to AWS S3. This package provides both a command-line interface and a Python API for automating MongoDB backup workflows.

## Features

- **MongoDB Backup**: Export MongoDB collections to JSON files with efficient batch processing
- **S3 Upload**: Upload backup files to AWS S3 buckets
- **Flexible Configuration**: Support for environment variables and command-line arguments
- **Memory Efficient**: Uses cursor-based pagination for large collections
- **CLI Tool**: Easy-to-use command-line interface
- **Python API**: Programmatic access for integration into your applications

## Installation

Install the package using pip:

```bash
pip install mongodb-backup-s3
```

## Requirements

- Python 3.8 or higher
- MongoDB database (local or remote)
- AWS S3 bucket and credentials (for S3 upload functionality)

## Quick Start

### 1. Using the Command-Line Interface

After installation, you can use the `mongodb-backup-s3` command from anywhere in your terminal.

#### Basic Usage

**Backup and upload to S3:**
```bash
mongodb-backup-s3 --mongo-uri mongodb://localhost:27017/ --db-name my_database \
  --aws-access-key YOUR_ACCESS_KEY --aws-secret-key YOUR_SECRET_KEY \
  --s3-bucket my-backup-bucket
```

**Backup only (save to local directory):**
```bash
mongodb-backup-s3 --action backup --mongo-uri mongodb://localhost:27017/ \
  --db-name my_database --output-dir ./backups
```

**Upload existing backup to S3:**
```bash
mongodb-backup-s3 --action upload --aws-access-key YOUR_ACCESS_KEY \
  --aws-secret-key YOUR_SECRET_KEY --s3-bucket my-backup-bucket \
  --output-dir ./backups
```

#### Using Environment Variables

Create a `.env` file in your project directory:

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
DB_NAME=my_database
OUTPUT_DIR=backups/mongodb_backup

# AWS Configuration
AWS_ACCESS_KEY=your_access_key_here
AWS_SECRET_KEY=your_secret_key_here
S3_BUCKET=my-backup-bucket
```

Then run the command without specifying credentials:

```bash
mongodb-backup-s3 --action both
```

#### Command-Line Arguments

| Argument | Description | Default | Required |
|----------|-------------|---------|----------|
| `--mongo-uri` | MongoDB connection URI | From `.env` or environment | For backup |
| `--db-name` | Name of the MongoDB database | From `.env` or environment | For backup |
| `--output-dir` | Directory to store backup files | `backups/mongodb_backup` | No |
| `--aws-access-key` | AWS Access Key ID | From `.env` or environment | For upload |
| `--aws-secret-key` | AWS Secret Access Key | From `.env` or environment | For upload |
| `--s3-bucket` | S3 bucket name | From `.env` or environment | For upload |
| `--action` | Action to perform: `backup`, `upload`, or `both` | `both` | No |

### 2. Using the Python API

You can also use this package programmatically in your Python code:

```python
from mongodb_backup_s3 import backup_mongodb, upload_to_s3

# Backup MongoDB database
backup_mongodb(
    mongo_uri="mongodb://localhost:27017/",
    db_name="my_database",
    output_dir="./backups",
    batch_size=1000  # Optional: documents per batch
)

# Upload backup to S3
upload_to_s3(
    aws_access_key="YOUR_ACCESS_KEY",
    aws_secret_key="YOUR_SECRET_KEY",
    s3_bucket="my-backup-bucket",
    backup_folder="./backups"
)
```

#### API Reference

##### `backup_mongodb(mongo_uri, db_name, output_dir, batch_size=1000)`

Backs up a MongoDB database to JSON files.

**Parameters:**
- `mongo_uri` (str): MongoDB connection URI (e.g., `mongodb://localhost:27017/`)
- `db_name` (str): Name of the database to backup
- `output_dir` (str): Directory path where backup files will be saved
- `batch_size` (int, optional): Number of documents to process per batch. Default: 1000

**Returns:** None

**Raises:** Prints error messages if connection or backup fails

**Example:**
```python
from mongodb_backup_s3 import backup_mongodb

backup_mongodb(
    mongo_uri="mongodb://user:password@host:27017/",
    db_name="production_db",
    output_dir="/path/to/backups",
    batch_size=5000
)
```

##### `upload_to_s3(aws_access_key, aws_secret_key, s3_bucket, backup_folder)`

Uploads backup files from a local directory to an AWS S3 bucket.

**Parameters:**
- `aws_access_key` (str): AWS Access Key ID
- `aws_secret_key` (str): AWS Secret Access Key
- `s3_bucket` (str): Name of the S3 bucket
- `backup_folder` (str): Path to the directory containing backup files

**Returns:** None

**Raises:** Prints error messages if credentials are invalid or upload fails

**Example:**
```python
from mongodb_backup_s3 import upload_to_s3

upload_to_s3(
    aws_access_key="AKIAIOSFODNN7EXAMPLE",
    aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    s3_bucket="my-backup-bucket",
    backup_folder="/path/to/backups"
)
```

## How It Works

### Backup Process

1. **Connection**: Connects to MongoDB using the provided URI
2. **Collection Discovery**: Lists all collections in the specified database
3. **Batch Processing**: For each collection:
   - Counts total documents
   - Processes documents in batches (default: 1000 per batch)
   - Writes documents as JSON arrays to `{collection_name}.json` files
4. **Output**: Creates JSON files in the specified output directory, one file per collection

### Upload Process

1. **S3 Client**: Initializes AWS S3 client with provided credentials
2. **File Discovery**: Walks through the backup directory
3. **Upload**: Uploads each JSON file to S3, preserving the directory structure
4. **Verification**: Prints confirmation for each successfully uploaded file

## Output Format

Each MongoDB collection is backed up as a JSON file containing an array of documents:

```json
[
  {"_id": {"$oid": "..."}, "field1": "value1", ...},
  {"_id": {"$oid": "..."}, "field1": "value2", ...},
  ...
]
```

The files use MongoDB's extended JSON format (with `$oid`, `$date`, etc.) to preserve data types.

## Examples

### Example 1: Complete Backup Workflow

```python
from mongodb_backup_s3 import backup_mongodb, upload_to_s3
import os
from dotenv import load_dotenv

load_dotenv()

# Backup
backup_mongodb(
    mongo_uri=os.getenv("MONGO_URI"),
    db_name=os.getenv("DB_NAME"),
    output_dir="./backups"
)

# Upload to S3
upload_to_s3(
    aws_access_key=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_key=os.getenv("AWS_SECRET_KEY"),
    s3_bucket=os.getenv("S3_BUCKET"),
    backup_folder="./backups"
)
```

### Example 2: Scheduled Backups

```python
import schedule
import time
from mongodb_backup_s3 import backup_database, upload_to_s3

def daily_backup():
    output_dir = f"./backups/{time.strftime('%Y%m%d')}"
    backup_mongodb(
        mongo_uri="mongodb://localhost:27017/",
        db_name="my_database",
        output_dir=output_dir
    )
    upload_to_s3(
        aws_access_key="YOUR_KEY",
        aws_secret_key="YOUR_SECRET",
        s3_bucket="my-backup-bucket",
        backup_folder=output_dir
    )

# Schedule daily backup at 2 AM
schedule.every().day.at("02:00").do(daily_backup)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Example 3: CLI with Environment Variables

```bash
# Set environment variables
export MONGO_URI="mongodb://localhost:27017/"
export DB_NAME="my_database"
export AWS_ACCESS_KEY="your_key"
export AWS_SECRET_KEY="your_secret"
export S3_BUCKET="my-bucket"

# Run backup and upload
mongodb-backup-s3 --action both
```

## Error Handling

The package includes error handling for common scenarios:

- **MongoDB Connection Errors**: Displays connection error messages
- **Missing Credentials**: Validates required parameters before execution
- **File System Errors**: Handles missing directories and file access issues
- **AWS Credential Errors**: Detects and reports invalid AWS credentials
- **S3 Upload Errors**: Provides detailed error messages for failed uploads

## Best Practices

1. **Use Environment Variables**: Store sensitive credentials in `.env` files (not in version control)
2. **Regular Backups**: Schedule regular backups for production databases
3. **Test Restores**: Periodically test restoring from backup files
4. **Monitor S3 Costs**: Be aware of S3 storage and transfer costs
5. **Secure Credentials**: Use IAM roles when possible instead of access keys
6. **Batch Size**: Adjust `batch_size` based on document size and available memory

## Troubleshooting

### Connection Issues

If you encounter MongoDB connection errors:
- Verify the MongoDB URI format
- Check network connectivity
- Ensure MongoDB is running and accessible
- Verify authentication credentials if required

### S3 Upload Issues

If S3 uploads fail:
- Verify AWS credentials are correct
- Check S3 bucket permissions
- Ensure the bucket exists and is accessible
- Verify IAM policies allow PutObject operations

### Memory Issues

For very large collections:
- Reduce `batch_size` parameter
- Ensure sufficient disk space for backup files
- Monitor system resources during backup

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/FarrukhShahid/mongodb-to-device-to-s3).

