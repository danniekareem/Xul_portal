from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pyodbc
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")


conn_string = f"DRIVER={DB_DRIVER};SERVER={DB_HOST};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"

try:
    conn = pyodbc.connect(conn_string)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")

    # Use this instead of pymssql connection