import mysql.connector
from src.config import db_config


class GenericModel:
    table_name = ""

    def __init__(self: object) -> None:
        try:
            self.cnx = mysql.connector.connect(
                user=db_config.USER_BD,
                password=db_config.PASSWD_BD,
                host=db_config.HOST_BD,
                database=db_config.DB_NAME,
            )
            self.cursor = self.cnx.cursor(dictionary=True)
        except mysql.connector.Error as err:
            self.msg = err
        else:
            self.msg = "OK"

    def end_connection(self: object):
        self.cursor.close()
        self.cnx.close()

    def insert_row(self: object, row: dict):
        # Afanado de https://dev.mysql.com/doc/connector-python/
        # en/connector-python-example-cursor-transaction.html
        columns = ", ".join(list(row.keys()))
        placeholder = ", ".join([f"%({key})s" for key in row.keys()])

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholder})"

        self.cursor.execute(query, row)
        self.curso.commit()

    @classmethod
    def map_result(model: object, result_row: dict) -> None:
        pass

    @classmethod
    def update_row(model: object, params: dict) -> None:
        return None
