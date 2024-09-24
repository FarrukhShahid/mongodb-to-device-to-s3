
# MongoDB Backup and S3 Upload Scripts

This project provides Python scripts to automate the backup of a MongoDB database and upload the backup files to an AWS S3 bucket. The project is structured to handle both tasks separately, with a parent script coordinating between the backup and upload operations.

## Features
- **Backup MongoDB Database**: Extracts data from MongoDB and stores it as JSON files in a JSON array format.
- **Upload to S3**: Uploads the MongoDB backup files to a specified AWS S3 bucket.
- **Environment Variable Support**: Easily configure MongoDB and AWS credentials using an `.env` file.
- **Command-line Flexibility**: You can pass arguments for MongoDB URI, AWS credentials, and backup folder at runtime.
- **Cursor-Based Pagination**: Backup is done in a memory-efficient way using MongoDB's cursor with pagination.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/mongodb-backup-s3.git
   cd mongodb-backup-s3
   ```

2. **Install dependencies**:
   Use the provided `requirements.txt` file to install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create an `.env` file**:
   Create a `.env` file in the root directory of your project to store the MongoDB URI, database name, and AWS credentials.
   ```bash
   touch .env
   ```

   Example `.env` file:
   ```
   # MongoDB Config
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=my_database

   # AWS Config
   AWS_ACCESS_KEY=your_access_key
   AWS_SECRET_KEY=your_secret_key
   S3_BUCKET=your_bucket_name

   # Backup Directory
   OUTPUT_DIR=mongodb_backup
   ```

## Usage

### 1. Backup Only

To perform a MongoDB backup and store the collections as JSON files:

```bash
python main.py --action backup
```

You can also override the `.env` values with command-line arguments:

```bash
python main.py --mongo-uri mongodb://localhost:27017/ --db-name my_database --output-dir my_backup --action backup
```

### 2. Upload to S3 Only

To upload the backup files to an S3 bucket:

```bash
python main.py --action upload
```

You can also provide AWS credentials and bucket name as arguments:

```bash
python main.py --aws-access-key your_access_key --aws-secret-key your_secret_key --s3-bucket your_bucket_name --output-dir my_backup --action upload
```

### 3. Backup and Upload

To perform both actions (backup and upload) in a single command:

```bash
python main.py --action both
```

### Command-line Arguments

- `--mongo-uri`: MongoDB connection URI (default: from `.env`).
- `--db-name`: Name of the MongoDB database (default: from `.env`).
- `--output-dir`: Directory to store the backup files (default: from `.env`).
- `--aws-access-key`: AWS Access Key for S3 (default: from `.env`).
- `--aws-secret-key`: AWS Secret Key for S3 (default: from `.env`).
- `--s3-bucket`: Name of the S3 bucket (default: from `.env`).
- `--action`: Choose between `backup`, `upload`, or `both` (default: `both`).

For full details on how to use the script, run:
```bash
python main.py --help
```

## Project Structure

```
mongodb-backup-s3/
│
├── backup_mongodb.py        # Script for backing up MongoDB
├── upload_to_s3.py          # Script for uploading backup to S3
├── main.py           # Parent script that handles argument parsing and runs backup/upload
├── .env                     # Environment file for configuration
├── requirements.txt         # List of required Python packages
└── README.md                # Project documentation
```

## Requirements

- Python 3.x
- MongoDB
- AWS S3 bucket and credentials
- Python packages (install via `requirements.txt`)

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Feel free to contribute to this project by submitting issues or pull requests!
