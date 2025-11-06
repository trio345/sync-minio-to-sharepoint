# db.py
import pymysql
from config import DB_CONFIG

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def init_db():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_sync_state (
            id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
            file_path VARCHAR(255) NOT NULL,
            source_id CHAR(36),
            source ENUM('minio', 'sharepoint') NOT NULL,
            last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    cursor.close()
    db.close()

def delete_row(cursor, checksum, file_path):
    cursor.execute("DELETE FROM file_sync_state WHERE checksum=%s AND file_path=%s", (checksum,file_path))
    cursor.close()

def file_exists(cursor, source_id):
    cursor.execute("SELECT file_path FROM file_sync_state WHERE source_id=%s", (source_id,))
    return cursor.fetchone()

def file_check_path(cursor, path):
    cursor.execute("SELECT file_path FROM file_sync_state WHERE file_path=%s", (path))
    return cursor.fetchone()

def upsert_file(cursor, path, source, source_id=""):
    cursor.execute("""
        INSERT INTO file_sync_state (file_path, source, source_id)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE source=%s
    """, (path, source, source_id, source))

