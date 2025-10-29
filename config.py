# config.py
GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"
HOSTNAME = 'sqqmy.sharepoint.com'
SITE_PATH = "TestISGS"

TENANT_ID = "01b81770-4c98-4845-8ba0-151c7b22f724"
CLIENT_ID = "f1579a3f-7ab3-4cbd-8236-eae27b8150ae"
CLIENT_SECRET = "ivP8Q~ZUZsh0Q_xyJlFCb40KPQUT8tJC3i~2ccVT"

MINIO_URL = "http://127.0.0.1:9000"
MINIO_ACCESSKEY = "minioadmin"
MINIO_SECRETKEY = "minioadmin"
MINIO_BUCKET = "portal"


# Spesify prefix folder in minio, exp: contract, contract/2024, portfolio
PREFIX_FOLDER = [
    'contract',
    'portfolio'
]

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "sync_db"
}
