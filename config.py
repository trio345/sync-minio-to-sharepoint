# config.py
GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"
HOSTNAME = '*'
SITE_PATH = "*"

TENANT_ID = "*"
CLIENT_ID = "*"
CLIENT_SECRET = "*"

MINIO_URL = "http://127.0.0.1:9000"
MINIO_ACCESSKEY = "minioadmin"
MINIO_SECRETKEY = "minioadmin"
MINIO_BUCKET = "portal"


# Spesify prefix folder in minio, exp: contract, contract/2024,portfolio
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
