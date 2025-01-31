import pymssql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Database connection using pymssql
def get_db():
    conn = pymssql.connect(
        server=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME    
    )
    try:
        yield conn
    finally:
        conn.close()
