# src/utils/db_helper.py
import mysql.connector
from mysql.connector import Error
from src.config.database import db_config

class DatabaseHelper:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**db_config)
            if self.connection.is_connected():
                print("Conexión exitosa a MySQL")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self.connection = None

    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return False
        finally:
            cursor.close()

    def fetch_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error al consultar datos: {e}")
            return []
        finally:
            cursor.close()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")