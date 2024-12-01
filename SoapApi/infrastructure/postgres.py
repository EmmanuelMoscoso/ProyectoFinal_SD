import os
import psycopg2

# Database configuration
DATABASE_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'soap_api'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'yourpassword'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432))
}

def get_connection():
    """Returns a new database connection."""
    return psycopg2.connect(**DATABASE_CONFIG)

def initialize_database():
    """Creates the necessary table if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            data JSONB NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
