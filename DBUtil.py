from utils import read_db_config
import mysql.connector
from mysql.connector import Error

db_config = read_db_config()


class DBUtil:
    def __init__(self, config=None):
        if config is None:
            config = db_config
        try:
            self.sql_conn = mysql.connector.connect(**config)
        except Error as error:
            print(error)
            exit(1)

    def is_connected(self) -> bool:
        return self.sql_conn.is_connected()

    def get_all_entries(self, table) -> list:
        cursor = self.sql_conn.cursor()
        cursor.execute(f'SELECT * FROM {table}')
        return cursor.fetchall()

    def get_all_gdp_entries(self) -> dict:
        return {key: value for key, value in self.get_all_entries('GDP').__reversed__()}

    def get_all_usd_entries(self) -> dict:
        return {key: value for key, value in self.get_all_entries('USD').__reversed__()}