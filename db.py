"""Database connection utilities for PostgreSQL"""

import os
import psycopg2

def get_postgres_connection():
    """Create and return a PostgreSQL database connection.
    Uses environment variable POSTGRES_HOST if set, otherwise defaults to localhost.
    """
    host = os.getenv("POSTGRES_HOST")
    if host is None:
        host = "localhost"

    conn = psycopg2.connect(f"host={host} dbname=db user=user password=password")
    return conn
