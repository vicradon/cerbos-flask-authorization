import os
import sqlite3
import argparse
import random
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('DB_PATH')

class Database:
    def __init__(self):
        self.db_path = db_path

    def fetch_rows(self, query, params=None):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute(query, params or [])
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            return [dict(zip(colnames, row)) for row in rows]
        except Exception as error:
            print(f"Error: {error}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def execute_query(self, query, params=None):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute(query, params or [])
            connection.commit()
            return cursor.rowcount
        except Exception as error:
            print(f"Error: {error}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


