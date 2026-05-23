"""
db.py — PostgreSQL connection and schema initialization
"""

import psycopg2
import os

# Update these with your PostgreSQL credentials
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "expense_analyzer"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "1234"),
    "port": os.getenv("DB_PORT", "5433")
}

def get_connection():
    """Return a new PostgreSQL connection."""
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            date VARCHAR(20),
            description TEXT,
            amount NUMERIC(12, 2),
            category VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_category ON transactions(category);
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")
