from dotenv import load_dotenv
import os

load_dotenv()
# config.py
GRAPH_API_BASE = os.getenv("GRAPH_API_BASE")
HOSTNAME = os.getenv("HOSTNAME")
SITE_PATH = os.getenv("SITE_PATH")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
MINIO_URL = os.getenv("MINIO_URL")
MINIO_ACCESSKEY = os.getenv("MINIO_ACCESSKEY")
MINIO_SECRETKEY = os.getenv("MINIO_SECRETKEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")
MINIO_REGION = os.getenv("MINIO_REGION")
PREFIX_FOLDER = os.getenv("PREFIX_FOLDER").split(", ")
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
