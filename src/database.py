
import psycopg2
from psycopg2.extras import execute_batch
import os

class Database:
    """
    A class to represent a database connection.
    """
    def __init__(self, host, dbname, user, password, port=5432):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
    
    # a method to connect to the database
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("Connected to PostgreSQL")
        except Exception as e:
            print("Connection failed:", e)

    # a method to execute a query
    def cursor(self):
        if self.conn:
            return self.conn.cursor()
        raise Exception("Database not connected")

    # a method to commit changes
    def commit(self):
        if self.conn:
            self.conn.commit()
    # a method to close the connection
    def close(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")
