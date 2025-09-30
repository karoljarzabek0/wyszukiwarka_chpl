import psycopg2
import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def log_query(conn, is_index: bool, query_name: str, slug: str = None):
    """
    Insert a log into the query_logs table.

    Args:
        is_index (bool): True if index page, False if product page
        query_name (str): Name of the executed query
        slug (str, optional): Product slug if applicable
    """
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO query_logs (is_index, query_name, slug)
            VALUES (%s, %s, %s)
            """,
            (is_index, query_name, slug)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed to log query: {e}")