import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorBufferedDict
from src.config import db_config


class ConnectionContext:
    cnx: MySQLConnection  # Representa una conexión a una base de datos
    cursor: MySQLCursorBufferedDict  # Para ejecutar operaciones en la bd
    msg: str

    def __init__(self) -> None:
        try:
            self.cnx = mysql.connector.connect(
                user=db_config.USER_BD,
                password=db_config.PASSWD_BD,
                host=db_config.HOST_BD,
                database=db_config.DB_NAME,
            )
            self.cursor = self.cnx.cursor(buffered=True, dictionary=True)
        except mysql.connector.Error as err:
            self.msg = err
        else:
            self.msg = "OK"

    def __enter__(self) -> object:
        return self

    # Cortamos la conexión cuando se va del scope
    def __exit__(self) -> None:
        self.cursor.close()
        self.cnx.close()

    def _execute(self, query: str, values: dict | None) -> bool:
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
        except mysql.connector.Error as err:
            self.msg = err
            self.cnx.rollback()
            return False
        else:
            self.cnx.commit()
            return True

    def get_all(self, table: str) -> dict | None:
        query = f"SELECT * FROM {table}"

        if not self._execute(query):
            return None

        return self.cursor.fetchall()

    def get_row(self, table, prim_keys: dict) -> dict | None:
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in prim_keys.keys()]
        )
        query = f"SELECT * FROM {table} WHERE {condition_placeholder}"

        if not self._execute(query, prim_keys):
            return None

        return self.cursor.fetchone()

    def insert_row(self, table, row: dict) -> bool:
        # Docs: https://dev.mysql.com/doc/connector-python/
        # en/connector-python-example-cursor-transaction.html
        columns = ", ".join(list(row.keys()))
        placeholder = ", ".join([f"%({key})s" for key in row.keys()])

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholder})"

        if not self._execute(query, row):
            return False

        return True

    def update_row(self, table, new_attributes: dict, prim_keys: dict) -> bool:
        placeholder = ", ".join([f"{key}=%({key})s" for key in new_attributes.keys()])
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in prim_keys.keys()]
        )

        query = f"UPDATE {table} SET ({placeholder}) WHERE ({condition_placeholder})"

        if not self._execute(query, {**new_attributes, **prim_keys}):
            return False

        return True

    def delete_row(self, table, prim_keys: dict) -> None:
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in prim_keys.keys()]
        )

        query = f"DELETE FROM {table} WHERE ({condition_placeholder})"

        if not self._execute(query, prim_keys):
            return False

        return True
