# main.py
from config import *
from db import init_db
from minio_utils import get_minio_client, get_all_minio_files, sync_minio_to_db
from sharepoint_utils import get_access_token, get_site_id, get_drive_id, get_all_files
from sync_job import run_sync, sync_sharepoint_to_db

def main():
    print("[SYNC JOB STARTED]")
    init_db()

    access_token = get_access_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    site_id = get_site_id(HOSTNAME, SITE_PATH, access_token)
    drive_id = get_drive_id(site_id, access_token)

    minio_client = get_minio_client(MINIO_URL, MINIO_ACCESSKEY, MINIO_SECRETKEY, MINIO_REGION)
    minio_data = get_all_minio_files(minio_client, MINIO_BUCKET)
    sp_data = get_all_files(drive_id, access_token)
    sync_minio_to_db(minio_data)
    sync_sharepoint_to_db(sp_data)    

    run_sync(minio_client, MINIO_BUCKET, drive_id, access_token, minio_data, sp_data)

    print("[✅ SYNC JOB COMPLETED]")

if __name__ == "__main__":
    main()
