import os
import bson.json_util as json_util
from pymongo import MongoClient

def backup_mongodb(mongo_uri, db_name, output_dir, batch_size=1000):
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return

    # Create backup directory if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over collections and backup data in batches
    try:
        collections = db.list_collection_names()
        print(f'Found {len(collections)} collections to backup')
        for collection_name in collections:
            collection = db[collection_name]
            total_docs = collection.count_documents({})  # Get the total number of documents
            print(f'Backing up {collection_name} collection with {total_docs} documents')

            # Open a file for writing and start the JSON array
            with open(f'{output_dir}/{collection_name}.json', 'w') as f:
                f.write('[')  # Start of JSON array
                
                first = True  # To keep track of first document for proper comma placement
                for skip in range(0, total_docs, batch_size):
                    cursor = collection.find({}).skip(skip).limit(batch_size)  # Use skip and limit for pagination
                    
                    for document in cursor:
                        if not first:
                            f.write(',')  # Add a comma before subsequent documents
                        f.write(json_util.dumps(document))  # Write the document
                        first = False  # Set to False after writing the first document

                f.write(']')  # End of JSON array

            print(f'Backup complete for collection: {collection_name}')

        print(f'Backup complete. Backup stored in directory: {output_dir}')
    except Exception as e:
        print(f"Error during backup: {str(e)}")
