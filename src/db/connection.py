import mysql.connector
from src.config import db_config

"""
 Author: Ezequiel Gonzalez
 Description: This class is responsible for establishing a connection to the database
 Date: 2021-10-18
 """
class Connection:
    def __init__(self: object) -> object:
        try:
            self.cnx = mysql.connector.connect(
                user=db_config.USER_BD,
                password=db_config.PASSWD_BD,
                host=db_config.HOST_BD,
                database=db_config.DB_NAME
            )
            self.cursor = self.cnx.cursor(dictionary=True)
        except mysql.connector.Error as err:
            self.msg = err
        else:
            self.msg = "OK"

    def run_query(self: object, query: str):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            return err

    def end_connection(self: object):
        self.cursor.close()
        self.cnx.close()