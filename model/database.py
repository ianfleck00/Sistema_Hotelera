
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class DatabaseManager:
    def __init__(self, config=DB_CONFIG):
        self.config = config
        self.conn = None

class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",       
            password="Root2025",       
            database="hotel_bd" 
        )
        self.conn.autocommit = True

    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or ())
        finally:
            cursor.close()

    def fetchall(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or ())
            # Devolver como lista de tuplas
            return cursor.fetchall()
        finally:
            cursor.close()

    def fetchone(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or ())
            # Devolver como tupla
            return cursor.fetchone()
        finally:
            cursor.close()
