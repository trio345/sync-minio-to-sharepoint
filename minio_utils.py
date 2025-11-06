# minio_utils.py
from config import *
from db import get_db_connection, upsert_file
import boto3
import hashlib


def get_minio_client(endpoint, access_key, secret_key, region_name):
    return boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name
    )

def get_all_minio_files(client, bucket):
    all_files = []
    prefixes = PREFIX_FOLDER
    if prefixes is None:
        prefixes = [""]

    for prefix in prefixes:
        if not isinstance(prefix, str):
            raise TypeError(f"Prefix harus string!")

        objects = client.list_objects_v2(Bucket=bucket, Prefix=prefix).get("Contents", [])
        for obj in objects:
            all_files.append({
                "name": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"]
            })

    return all_files

def read_minio_file(client, bucket, path):
    obj = client.get_object(Bucket=bucket, Key=path)
    return obj["Body"].read()

def generate_minio_id(file_path):
    return hashlib.md5(file_path.encode()).hexdigest()

def sync_minio_to_db(minio_data):
    print("🔄 Mulai sinkronisasi MinIO ke Database...")
    db = get_db_connection()
    cursor = db.cursor()

    minio_paths = {obj["name"] for obj in minio_data}

    cursor.execute("SELECT file_path FROM file_sync_state WHERE source = 'minio'")
    db_files = {row[0] for row in cursor.fetchall()}

    new_files = minio_paths - db_files    
    for file_path in new_files:
        source_id = generate_minio_id(file_path)
        upsert_file(cursor, file_path, 'minio', source_id)
    
    removed_files = db_files - minio_paths
    for file_path in removed_files:
        cursor.execute("DELETE FROM file_sync_state WHERE file_path = %s AND source = 'minio'", (file_path,))

    db.commit()
    cursor.close()
    db.close()
    print("✅ Sinkronisasi MinIO → Database selesai.")

