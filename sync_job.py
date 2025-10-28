# sync_job.py
import hashlib
import requests
from config import *
from db import get_db_connection, file_exists, upsert_file,delete_row
from minio_utils import generate_minio_id
from sharepoint_utils import upload_file, set_metadata

def calculate_checksum(data):
    return hashlib.sha256(data).hexdigest()

def delete_from_sharepoint(drive_id, access_token, file_path, source):
    if source != 'minio':
        return

    print(f"🗑️ Menghapus {file_path} dari SharePoint (asal MinIO)")
    delete_url = f"{GRAPH_API_BASE}/drives/{drive_id}/root:/{file_path}"
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.delete(delete_url, headers=headers)

    if res.status_code in (200, 201):
        print(f"File {file_path} berhasil dihapus")
    else:
        print(f"File {file_path} gagal dihapus")


def sync_sharepoint_to_db(sp_data):
    db = get_db_connection()
    cursor = db.cursor()
    for path, sp in sp_data.items():
        source_id = sp.get('source_id')
        if not source_id:
            record = file_exists(cursor, path)
            if not record:
                upsert_file(cursor, path, 'sharepoint', None)
                print(f"File baru dari Sharepoint ditambahkan ke DB {path}")
            else:
                print(f"File {path} dari Sharepoint sudah ada di DB")
        else:
            pass
    db.commit()
    cursor.close()
    db.close()

def run_sync(minio_client, bucket, drive_id, access_token, minio_data, sp_data):
    db = get_db_connection()
    cursor = db.cursor()

    # Upload/update minio ke sharepoint
    for obj in minio_data:
        file_path = obj["name"]
        file_data = minio_client.get_object(Bucket=bucket, Key=file_path)["Body"].read()
        source_id = generate_minio_id(file_path)
        record = file_exists(cursor, source_id)

        if not record:
            print(f"🆕 Upload baru dari MinIO: {file_path}")
            item_id = upload_file(drive_id, access_token, file_path, file_data)
            set_metadata(drive_id, access_token, item_id, source_id)
            upsert_file(cursor, file_path, 'minio', source_id)
        else: pass
    # Hapus file yang ada di sharepoint namun tidak ada di minio
    # print("SPDATA", sp_data)
    for path, sp in sp_data.items():
        source_id = sp.get('source_id')
        record = file_exists(cursor, source_id)
        if not record:
            delete_from_sharepoint(drive_id, access_token, path, 'minio')

    db.commit()
    cursor.close()
    db.close()
